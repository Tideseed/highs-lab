#!/usr/bin/env python3
"""MIPFEAS-style primal integral (Mittelmann, https://plato.asu.edu/ftp/mipfeas.html) on existing result dirs.

  bench/primal.py <result-dir> [--control dev] [--md out.md] [--boot 5000]

Mittelmann's per-run score is P = (1/T) * integral_0^T p(t) dt with
  p(t) = 2 while there is no incumbent, 1 if z(t)*z* < 0, else |z(t) - z*| / max(|z(t)|, |z*|, 1)
and solvers are ranked by the shifted geometric mean of P (shift 0.001). z* comes from solu.txt (=opt= and =best=);
instances without a finite reference are skipped (MIPFEAS uses only feasible instances).

Only the primal column of the logged trajectory is used; the final primal bound is appended at solver_time, and nothing
is credited beyond T (as in hard.py). Like PDGI this is an ESTIMATE from sparse logged rows: incumbent changes between
rows are not observed, and the bootstrap does not quantify that measurement error. T is OUR time limit (300 s, 1 thread, X925 core), not MIPFEAS's 600 s / 24 threads:
absolute values are not comparable with the published table, only arms on the same data are.
"""
from __future__ import annotations

import argparse
import json
import math
import random
from collections import defaultdict
from pathlib import Path

from analyze import load_solu

SHIFT = 0.001


def p_value(z: float | None, zs: float) -> float:
    if z is None or not math.isfinite(z):
        return 2.0
    if z * zs < 0:
        return 1.0
    return abs(z - zs) / max(abs(z), abs(zs), 1.0)


def primal_obs(r: dict) -> list[tuple[float, float | None]]:
    obs = sorted(((row[0], row[2]) for row in r.get("trajectory", []) if row[0] is not None), key=lambda o: o[0])
    if r.get("solver_time") is not None and r.get("primal_bound") is not None:
        obs.append((float(r["solver_time"]), r["primal_bound"]))
        obs.sort(key=lambda o: o[0])
    return obs


def primal_integral(r: dict, zs: float) -> float:
    T = float(r["time_limit"])
    area, t_prev, p_prev = 0.0, 0.0, 2.0
    for t, z in primal_obs(r):
        t = min(float(t), T)
        area += p_prev * max(0.0, t - t_prev)
        t_prev, p_prev = max(t_prev, t), p_value(z, zs)
        if t >= T:
            break
    area += p_prev * max(0.0, T - t_prev)
    return area / T


def first_time(r: dict, zs: float, tol: float | None) -> float | None:
    """Time of the first incumbent (tol None) or of the first incumbent within tol of z*; None if never within T."""
    T = float(r["time_limit"])
    for t, z in primal_obs(r):
        if t > T:
            return None
        if z is not None and math.isfinite(z) and (tol is None or p_value(z, zs) <= tol):
            return float(t)
    return None


def feasible_by_t(r: dict) -> bool:
    """An incumbent existed within the horizon T (a finite final bound found after T does not count)."""
    T = float(r["time_limit"])
    return any(z is not None and math.isfinite(z) and t <= T for t, z in primal_obs(r))


def feasible_at_end(r: dict) -> bool:
    return r.get("primal_bound") is not None and math.isfinite(r["primal_bound"])


def sgm(xs: list[float], shift: float) -> float:
    return math.exp(sum(math.log(x + shift) for x in xs) / len(xs)) - shift


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("dir")
    ap.add_argument("--control", default="dev")
    ap.add_argument("--md")
    ap.add_argument("--boot", type=int, default=5000)
    a = ap.parse_args()
    ref = {k: v for k, (v, _) in load_solu().items() if math.isfinite(v)}
    runs = [json.loads(p.read_text()) for p in Path(a.dir).glob("*.json")
            if not p.name.startswith("RESOURCES") and not p.name.endswith(".stale.json")]
    runs = [r for r in runs if r["instance"] in ref]
    by = defaultdict(dict)
    for r in runs:
        by[(r["instance"], r["seed"])][r["arm"]] = r
    arms = sorted({r["arm"] for r in runs})
    T = {r["time_limit"] for r in runs}
    out = [f"# MIPFEAS-style primal integral `{a.dir}` (control `{a.control}`)", "",
           f"{len(runs)} runs on instances with a finite reference value; T = {', '.join(map(str, sorted(T)))} s. "
           "Score per run: Mittelmann's primal integral P in [0, 2] (lower is better); table: shifted geometric mean "
           f"(shift {SHIFT}) over instances (seeds averaged first), ratio vs control with a paired instance bootstrap.", "",
           "| arm | inst | SGM P | ratio vs ctl [95% CI] | mean P | incumbent by T | feasible at termination "
           "| SGM t first incumbent (s, found only) | within 1 % of z* by T | within 1e-4 by T |", "|---" * 10 + "|"]
    no_inc = defaultdict(list)
    per_inst_all = {}
    for arm in arms:
        pairs = defaultdict(lambda: ([], []))
        for (inst, seed), d in by.items():
            if arm in d and a.control in d:
                pairs[inst][0].append(primal_integral(d[arm], ref[inst]))
                pairs[inst][1].append(primal_integral(d[a.control], ref[inst]))
        insts = sorted(pairs)
        if not insts:
            continue
        pa = [sum(pairs[i][0]) / len(pairs[i][0]) for i in insts]
        pc = [sum(pairs[i][1]) / len(pairs[i][1]) for i in insts]
        per_inst_all[arm] = dict(zip(insts, zip(pa, pc)))
        ratio = sgm(pa, SHIFT) / sgm(pc, SHIFT)
        rng = random.Random(0)
        boots = []
        for _ in range(a.boot if arm != a.control else 0):
            idx = [rng.randrange(len(insts)) for _ in insts]
            boots.append(sgm([pa[k] for k in idx], SHIFT) / sgm([pc[k] for k in idx], SHIFT))
        boots.sort()
        ci = (boots[int(0.025 * len(boots))], boots[int(0.975 * len(boots)) - 1]) if boots else (1.0, 1.0)
        ar = [d[arm] for d in by.values() if arm in d and a.control in d]
        feas = sum(1 for r in ar if feasible_at_end(r))
        byt = sum(1 for r in ar if feasible_by_t(r))
        t1 = [t for r in ar if (t := first_time(r, ref[r["instance"]], None)) is not None]
        w1 = sum(1 for r in ar if first_time(r, ref[r["instance"]], 0.01) is not None)
        w4 = sum(1 for r in ar if first_time(r, ref[r["instance"]], 1e-4) is not None)
        for r in ar:
            if first_time(r, ref[r["instance"]], None) is None:
                no_inc[arm].append(f"{r['instance']} s{r['seed']}")
        out.append(f"| {arm} | {len(insts)} | {sgm(pa, SHIFT):.4f} | {ratio:.3f} [{ci[0]:.3f}, {ci[1]:.3f}] | "
                   f"{sum(pa) / len(pa):.4f} | {byt}/{len(ar)} | {feas}/{len(ar)} | {sgm(t1, 1.0) if t1 else float('nan'):.1f} | "
                   f"{w1}/{len(ar)} | {w4}/{len(ar)} |")
    out += ["", "## Runs with no incumbent by T", ""]
    for arm in arms:
        out.append(f"- **{arm}** ({len(no_inc[arm])}): " + ", ".join(sorted(no_inc[arm])))
    out += ["", "## Largest per-instance differences (|ΔP| ≥ 0.05, seed mean)", "", "| arm | instance | P arm | P ctl | ΔP |",
            "|---|---|---|---|---|"]
    for arm, d in per_inst_all.items():
        if arm == a.control:
            continue
        for i, (x, y) in sorted(d.items(), key=lambda kv: kv[1][0] - kv[1][1]):
            if abs(x - y) >= 0.05:
                out.append(f"| {arm} | {i} | {x:.3f} | {y:.3f} | {x - y:+.3f} |")
    text = "\n".join(out)
    print(text)
    if a.md:
        Path(a.md).write_text(text + "\n")


if __name__ == "__main__":
    main()
