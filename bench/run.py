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


def parse_log(text: str) -> dict:
    out: dict = {}
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


def run_job(job: dict, core_pool: "queue.Queue[int]", mem_cap: str, out_dir: Path) -> dict:
    res_path = out_dir / f"{job['arm']}__{job['instance']}__s{job['seed']}.json"
    if res_path.exists():
        return json.loads(res_path.read_text())
    core = core_pool.get()
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
        t0 = time.time()
        # A hard wall-clock guard far above the limit: a solver that ignores time_limit is itself a finding (overrun),
        # but the harness must not hang forever.
        guard = job["time_limit"] * 4 + 600
        try:
            p = subprocess.run(cmd, capture_output=True, text=True, timeout=guard)
            rc, timed_out = p.returncode, False
            stdout = p.stdout
        except subprocess.TimeoutExpired as e:
            rc, timed_out = None, True
            stdout = (e.stdout or b"").decode() if isinstance(e.stdout, bytes) else (e.stdout or "")
        wall = time.time() - t0
        (work / "stdout.txt").write_text(stdout or "")
        rec = {k: job[k] for k in ("arm", "instance", "seed", "time_limit", "binary_sha")}
        rec.update(core=core, wall=wall, overrun=wall - job["time_limit"], rc=rc, harness_timeout=timed_out,
                   options=job["options"], has_solution=sol.exists())
        rec.update(parse_log(stdout or ""))
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
    ap.add_argument("--out", required=True)
    ap.add_argument("--shuffle-seed", type=int, default=12345)
    a = ap.parse_args()

    arms = tomllib.loads(Path(a.arms).read_text())
    if a.only_arms:
        arms = {k: v for k, v in arms.items() if k in a.only_arms}
    for name, arm in arms.items():
        arm["binary"] = str(Path(arm["binary"]).expanduser())
        arm["sha"] = sha256(Path(arm["binary"]))
    names = [l.strip() for l in Path(a.set).read_text().splitlines() if l.strip() and not l.startswith("#")]
    out = Path(a.out)
    out.mkdir(parents=True, exist_ok=True)

    rng = random.Random(a.shuffle_seed)
    jobs = []
    for inst in names:
        path = INST_DIR / f"{inst}.mps.gz"
        if not path.exists():
            sys.exit(f"missing instance {path}")
        for seed in a.seeds:
            order = list(arms)
            rng.shuffle(order)
            for arm in order:
                jobs.append(dict(arm=arm, instance=inst, seed=seed, path=path, time_limit=a.time_limit,
                                 binary=arms[arm]["binary"], binary_sha=arms[arm]["sha"],
                                 options=arms[arm].get("options", {})))

    cores = parse_cores(a.cores)
    meta = dict(started=time.strftime("%Y-%m-%dT%H:%M:%S%z"), argv=sys.argv, cores=cores, mem_cap=a.mem_cap,
                arms={k: {"binary": v["binary"], "sha": v["sha"], "options": v.get("options", {})}
                      for k, v in arms.items()},
                n_jobs=len(jobs), loadavg=os.getloadavg(),
                meminfo_available_kb=int(re.search(r"MemAvailable:\s+(\d+)", Path("/proc/meminfo").read_text())[1]),
                serving_units={u: subprocess.run(["systemctl", "--user", "is-active", u], capture_output=True,
                                                 text=True).stdout.strip()
                               for u in ("ornith-vllm", "llama-qwen38")})
    (out / f"RESOURCES-{time.strftime('%Y%m%d-%H%M%S')}.json").write_text(json.dumps(meta, indent=1))

    pool: "queue.Queue[int]" = queue.Queue()
    for c in cores:
        pool.put(c)
    done = 0
    lock = threading.Lock()
    with cf.ThreadPoolExecutor(max_workers=len(cores)) as ex:
        futs = [ex.submit(run_job, j, pool, a.mem_cap, out) for j in jobs]
        for f in cf.as_completed(futs):
            r = f.result()
            with lock:
                done += 1
                print(f"[{done}/{len(jobs)}] {r['arm']:<16} {r['instance']:<28} s{r['seed']} "
                      f"{r.get('status', r.get('lp_status', '?')):<20} wall={r['wall']:.1f}", flush=True)
    print("DONE", out)


if __name__ == "__main__":
    main()
