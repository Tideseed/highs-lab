#!/usr/bin/env python3
"""Benchmark runner for HiGHS arms.

Runs every (instance, seed, arm) job once, pinned to one core with a hard memory cap, and writes one JSON result per
job. Resumable: a job whose result file exists is skipped. Arms of the same instance+seed are queued next to each
other in a shuffled order so that drift and contention hit all arms alike.

  bench/run.py --arms bench/arms.toml --set bench/sets/screen-v0.txt --seeds 0 1 2 --time-limit 300 \
      --cores 5-9,15-19 --out bench/results/raw/<run-id>

arms.toml:
  [dev]
  binary = "~/git_repositories/highs-builds/dev/bin/highs"
  [dev-tideseed]
  binary = "..."
  options = { mip_heuristic_run_zi_round = true }    # optional HiGHS options, written to an options file
"""
from __future__ import annotations

import argparse
import concurrent.futures as cf
import hashlib
import json
import os
import queue
import random
import re
import shutil
import subprocess
import sys
import threading
import time
import tomllib
from pathlib import Path

INST_DIR = Path(os.environ.get("HIGHS_LAB_INSTANCES", "~/data/optopt/miplib/inst")).expanduser()


def parse_cores(spec: str) -> list[int]:
    cores: list[int] = []
    for part in spec.split(","):
        if "-" in part:
            a, b = part.split("-")
            cores += list(range(int(a), int(b) + 1))
        else:
            cores.append(int(part))
    return cores


def build_sha(binary: str) -> str:
    """Hash of the highs executable together with the libhighs it loads (the solver lives in the library)."""
    b = Path(binary)
    h = hashlib.sha256(sha256(b).encode())
    for lib in sorted((b.parent.parent / "lib").glob("libhighs.so*")):
        if lib.is_file() and not lib.is_symlink():
            h.update(sha256(lib).encode())
    return h.hexdigest()[:16]


def build_info(binary: str) -> dict:
    """Source SHA, compiler and effective flags from the CMake build directory of the binary."""
    bdir = Path(binary).parent.parent
    info = {"build_dir": str(bdir)}
    cache = bdir / "CMakeCache.txt"
    if cache.exists():
        wanted = {"CMAKE_BUILD_TYPE", "CMAKE_CXX_COMPILER", "CMAKE_CXX_FLAGS", "CMAKE_C_FLAGS",
                  "CMAKE_HOME_DIRECTORY", "CMAKE_INTERPROCEDURAL_OPTIMIZATION", "BUILD_SHARED_LIBS"}
        for line in cache.read_text().splitlines():
            key = line.split(":")[0]
            if key in wanted and "=" in line:
                info[key] = line.split("=", 1)[1]
    flags = bdir / "highs/CMakeFiles/highs.dir/flags.make"
    if flags.exists():
        m = re.search(r"^CXX_FLAGS = (.*)$", flags.read_text(), re.M)
        if m:
            info["effective_cxx_flags"] = m.group(1).strip()
    src = info.get("CMAKE_HOME_DIRECTORY")
    if src:
        r = subprocess.run(["git", "-C", src, "rev-parse", "HEAD"], capture_output=True, text=True)
        info["source_sha"] = r.stdout.strip()
        r = subprocess.run(["git", "-C", src, "status", "--porcelain", "--untracked-files=no"], capture_output=True, text=True)
        info["source_dirty"] = bool(r.stdout.strip())
    comp = info.get("CMAKE_CXX_COMPILER")
    if comp:
        r = subprocess.run([comp, "--version"], capture_output=True, text=True)
        info["compiler_version"] = r.stdout.splitlines()[0] if r.stdout else ""
    return info


SERVING_UNITS = ("ornith-vllm", "llama-qwen38")


def serving_state() -> dict:
    """State of the local LLM servers at the end of a job (they share memory bandwidth with the solver)."""
    return {u: subprocess.run(["systemctl", "--user", "is-active", u], capture_output=True, text=True).stdout.strip()
            for u in SERVING_UNITS}


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()[:16]


NUM = r"([-+]?(?:inf|\d+(?:\.\d*)?(?:[eE][-+]?\d+)?))"
PATTERNS = {
    "status": re.compile(r"^\s*Status\s+(.+?)\s*$", re.M),
    "primal_bound": re.compile(r"^\s*Primal bound\s+" + NUM, re.M),
    "dual_bound": re.compile(r"^\s*Dual bound\s+" + NUM, re.M),
    "gap": re.compile(r"^\s*Gap\s+(\S+)", re.M),
    "pd_integral": re.compile(r"^\s*P-D integral\s+" + NUM, re.M),
    "solver_time": re.compile(r"^\s*Timing\s+" + NUM, re.M),
    "presolve_time": re.compile(r"^\s+" + NUM + r" \(presolve\)", re.M | re.I),
    "nodes": re.compile(r"^\s*Nodes\s+(\d+)", re.M),
    "lp_iterations": re.compile(r"^\s*LP iterations\s+(\d+)", re.M),
    # LP-only runs
    "lp_status": re.compile(r"^Model status\s*:\s*(.+?)\s*$", re.M),
    "simplex_iterations": re.compile(r"^Simplex\s+iterations:\s*(\d+)", re.M),
    "objective": re.compile(r"^Objective value\s*:\s*" + NUM, re.M),
    "lp_time": re.compile(r"^HiGHS run time\s*:\s*" + NUM, re.M),
}


# progress rows of the MIP log: ... | BestBound BestSol Gap | Cuts InLp Confl. | LpIters Time
PROGRESS = re.compile(r"^\s*[A-Za-z]?\s+\d+\s+\d+\s+\d+\s+[\d.]+%\s+(\S+)\s+(\S+)\s+\S+\s+\d+\s+\d+\s+\d+"
                      r"\s+\d+\s+([\d.]+)s\s*$", re.M)


def to_float(x: str) -> float | None:
    try:
        return float(x)
    except ValueError:
        return None


def parse_log(text: str) -> dict:
    out: dict = {}
    traj = []
    for m in PROGRESS.finditer(text):
        d, p, t = to_float(m.group(1)), to_float(m.group(2)), to_float(m.group(3))
        traj.append([t, d, p])
    if traj:
        out["trajectory"] = traj
    for key, pat in PATTERNS.items():
        m = pat.findall(text)
        if not m:
            continue
        v = m[-1]
        if key in ("status", "lp_status", "gap"):
            out[key] = v
        elif key in ("nodes", "lp_iterations", "simplex_iterations"):
            out[key] = int(v)
        else:
            out[key] = float(v)
    return out


ADMIT_LOCK = threading.Lock()


def mem_available_gb() -> float:
    return int(re.search(r"MemAvailable:\s+(\d+)", Path("/proc/meminfo").read_text())[1]) / 1048576


def cap_gb(mem_cap: str) -> float:
    m = re.fullmatch(r"(\d+(?:\.\d+)?)([KMGT]?)", mem_cap.strip().upper())
    v, u = float(m.group(1)), m.group(2)
    return v * {"": 1 / 2**30, "K": 1 / 2**20, "M": 1 / 1024, "G": 1, "T": 1024}[u]


def admit(job: dict, need_gb: float, reserve_gb: float) -> None:
    """Block until launching one more run keeps MemAvailable >= reserve + the run's cap (memwatch floors: soft
    12 GiB sheds the interactive tier, hard 7 GiB sheds Agent Fast). Serialised so check and launch are atomic."""
    waited = False
    while True:
        avail = mem_available_gb()
        if avail >= reserve_gb + need_gb:
            if waited:
                print(f"admit: {job['arm']} {job['instance']} after throttling (MemAvailable {avail:.1f} GB)", flush=True)
            return
        if not waited:
            print(f"throttling: MemAvailable {avail:.1f} GB < reserve {reserve_gb} + cap {need_gb:.1f} GB; "
                  f"holding {job['arm']} {job['instance']}", flush=True)
            waited = True
        time.sleep(5)


def run_job(job: dict, core_pool: "queue.Queue[int]", mem_cap: str, out_dir: Path,
            reserve_gb: float = 20.0) -> dict:
    res_path = out_dir / f"{job['arm']}__{job['instance']}__s{job['seed']}.json"
    if res_path.exists():
        old = json.loads(res_path.read_text())
        if (old.get("binary_sha") == job["binary_sha"] and old.get("options") == job["options"]
                and old.get("time_limit") == job["time_limit"] and old.get("model_sha") == job["model_sha"]):
            return old
        res_path.rename(res_path.with_suffix(".stale.json"))
    core = core_pool.get()
    # the binary (or its shared library) must not change while a run set is in progress
    if build_sha(job["binary"]) != job["binary_sha"]:
        core_pool.put(core)
        raise RuntimeError(f"binary for arm {job['arm']} changed during the run set")
    try:
        work = out_dir / "work" / f"{job['arm']}__{job['instance']}__s{job['seed']}"
        work.mkdir(parents=True, exist_ok=True)
        opts = dict(job["options"])
        opts.setdefault("threads", 1)
        opts["time_limit"] = job["time_limit"]
        opts["random_seed"] = job["seed"]
        opts["log_file"] = str(work / "highs.log")
        (work / "options.txt").write_text("".join(f"{k} = {str(v).lower() if isinstance(v, bool) else v}\n"
                                                  for k, v in opts.items()))
        sol = work / "solution.sol"
        cmd = ["systemd-run", "--user", "--scope", "--quiet", "-p", f"MemoryMax={mem_cap}", "-p", "MemorySwapMax=0",
               "taskset", "-c", str(core), job["binary"], "--model_file", str(job["path"]),
               "--options_file", str(work / "options.txt"), "--solution_file", str(sol)]
        cmd = cmd[:1] + ["-p", "MemoryAccounting=yes"] + cmd[1:]
        cmd = [c for c in cmd]
        cmd.insert(cmd.index("taskset"), "/usr/bin/time")
        cmd.insert(cmd.index("taskset"), "-f")
        cmd.insert(cmd.index("taskset"), "PEAKRSS_KB=%M")
        with ADMIT_LOCK:
            admit(job, cap_gb(mem_cap), reserve_gb)
            t0 = time.time()
            proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            # give the run a moment to allocate before the next admission check
            time.sleep(1.0)
        # A hard wall-clock guard far above the limit: a solver that ignores time_limit is itself a finding (overrun),
        # but the harness must not hang forever.
        guard = job["time_limit"] * 4 + 600
        try:
            stdout, stderr = proc.communicate(timeout=max(1.0, guard - (time.time() - t0)))
            rc, timed_out = proc.returncode, False
        except subprocess.TimeoutExpired:
            proc.kill()
            stdout, stderr = proc.communicate()
            rc, timed_out = None, True
        m_rss = re.search(r"PEAKRSS_KB=(\d+)", stderr or "")
        wall = time.time() - t0
        (work / "stdout.txt").write_text(stdout or "")
        rec = {k: job[k] for k in ("arm", "instance", "seed", "time_limit", "binary_sha", "model_sha")}
        rec.update(serving_units=serving_state(), loadavg=os.getloadavg(),
                   peak_rss_gb=round(int(m_rss.group(1)) / 1048576, 3) if m_rss else None)
        rec.update(core=core, wall=wall, overrun=wall - job["time_limit"], rc=rc, harness_timeout=timed_out,
                   options=job["options"], has_solution=sol.exists())
        rec.update(parse_log(stdout or ""))
        # the model could not even be read within the time limit: not a solver crash
        rec["load_timeout"] = "Parser reached timeout" in (stdout or "")
        res_path.write_text(json.dumps(rec, indent=1))
        return rec
    finally:
        core_pool.put(core)


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--arms", required=True)
    ap.add_argument("--only-arms", nargs="*")
    ap.add_argument("--set", required=True, help="file with one instance name per line (without .mps.gz)")
    ap.add_argument("--seeds", type=int, nargs="+", default=[0])
    ap.add_argument("--time-limit", type=float, default=300)
    ap.add_argument("--cores", default="5-9,15-19", help="Cortex-X925 cores on the GB10 by default")
    ap.add_argument("--mem-cap", default="8G")
    ap.add_argument("--mem-reserve-gb", type=float, default=20.0,
                    help="keep at least this much MemAvailable (memwatch soft floor is 12 GiB)")
    ap.add_argument("--out", required=True)
    ap.add_argument("--shuffle-seed", type=int, default=12345)
    a = ap.parse_args()

    arms = tomllib.loads(Path(a.arms).read_text())
    if a.only_arms:
        arms = {k: v for k, v in arms.items() if k in a.only_arms}
    for name, arm in arms.items():
        arm["binary"] = str(Path(arm["binary"]).expanduser())
        arm["sha"] = build_sha(arm["binary"])
        arm["build"] = build_info(arm["binary"])
    names = [l.strip() for l in Path(a.set).read_text().splitlines() if l.strip() and not l.startswith("#")]
    out = Path(a.out)
    out.mkdir(parents=True, exist_ok=True)

    rng = random.Random(a.shuffle_seed)
    jobs = []
    for inst in names:
        path = INST_DIR / f"{inst}.mps.gz"
        if not path.exists():
            sys.exit(f"missing instance {path}")
        model_sha = sha256(path)
        for seed in a.seeds:
            order = list(arms)
            rng.shuffle(order)
            for arm in order:
                jobs.append(dict(arm=arm, instance=inst, seed=seed, path=path, time_limit=a.time_limit,
                                 binary=arms[arm]["binary"], binary_sha=arms[arm]["sha"], model_sha=model_sha,
                                 options=arms[arm].get("options", {})))

    cores = parse_cores(a.cores)
    # static budget: the caps of all concurrent runs must fit into MemAvailable minus the reserve
    budget = mem_available_gb() - a.mem_reserve_gb
    lanes = max(1, min(len(cores), int(budget // cap_gb(a.mem_cap)))) if budget > 0 else 1
    if lanes < len(cores):
        print(f"memory budget: MemAvailable-reserve = {budget:.1f} GB, cap {a.mem_cap} -> {lanes} lanes "
              f"instead of {len(cores)}", flush=True)
        cores = cores[:lanes]
    meta = dict(started=time.strftime("%Y-%m-%dT%H:%M:%S%z"), argv=sys.argv, cores=cores, mem_cap=a.mem_cap,
                mem_reserve_gb=a.mem_reserve_gb,
                arms={k: {"binary": v["binary"], "sha": v["sha"], "options": v.get("options", {}),
                          "build": v.get("build", {})}
                      for k, v in arms.items()},
                n_jobs=len(jobs), loadavg=os.getloadavg(),
                meminfo_available_kb=int(re.search(r"MemAvailable:\s+(\d+)", Path("/proc/meminfo").read_text())[1]),
                serving_units=serving_state())
    (out / f"RESOURCES-{time.strftime('%Y%m%d-%H%M%S')}.json").write_text(json.dumps(meta, indent=1))

    pool: "queue.Queue[int]" = queue.Queue()
    for c in cores:
        pool.put(c)
    done = 0
    lock = threading.Lock()
    with cf.ThreadPoolExecutor(max_workers=len(cores)) as ex:
        futs = [ex.submit(run_job, j, pool, a.mem_cap, out, a.mem_reserve_gb) for j in jobs]
        for f in cf.as_completed(futs):
            r = f.result()
            with lock:
                done += 1
                print(f"[{done}/{len(jobs)}] {r['arm']:<16} {r['instance']:<28} s{r['seed']} "
                      f"{r.get('status', r.get('lp_status', '?')):<20} wall={r['wall']:.1f}", flush=True)
    print("DONE", out)


if __name__ == "__main__":
    main()
