#!/usr/bin/env python3
"""Hard-instance comparison at a fixed time limit (instances rarely solve, so time-to-solve is uninformative).

  bench/hard.py <result-dir> [--control dev] [--md out.md] [--boot 5000]

Primary metric: our own primal-dual gap integral (PDGI), computed from the logged bound trajectory, not HiGHS's
reported "P-D integral" (which is 0 when the run never has both bounds, i.e. it scores "no information" as perfect).
  gap(t) = |p - d| / max(|p|, |d|), capped at 1;  gap(t) = 1 while either bound is missing (inf) or p*d < 0
  PDGI   = (1/T) * integral_0^T gap(t) dt  over the fixed horizon T = time limit, in [0, 1]; lower is better
Before the first logged row the gap is 1; after the last row the last gap holds until T (0 once solved).

Per arm vs control: mean PDGI and its paired difference with a bootstrap 95 % CI that resamples INSTANCES and keeps
each instance's seeds together; solved / feasible counts on the paired set; mean final gap; overrun past the limit
(reported separately, never mixed into PDGI); wrong answers vs solu.txt and crashes (any is a FAIL); reference
coverage (how many runs could be checked at all).
"""
from __future__ import annotations

import argparse
import json
import math
import random
from collections import defaultdict
from pathlib import Path

from analyze import load_solu, solved, wrong


def gap_value(d: float | None, p: float | None) -> float:
    if d is None or p is None or not math.isfinite(d) or not math.isfinite(p):
        return 1.0
    if d * p < 0:
        return 1.0
    den = max(abs(d), abs(p))
    if den == 0:
        return 0.0
    return min(1.0, abs(p - d) / den)


def pdgi(r: dict) -> float:
    T = float(r["time_limit"])
    traj = [row for row in r.get("trajectory", []) if row[0] is not None]
    if not traj:
        # no progress rows: fall back to the final bounds (a run solved at presolve has gap 0 from its end)
        g = gap_value(r.get("dual_bound"), r.get("primal_bound"))
        t_end = min(T, r.get("solver_time", T)) if solved(r) else T
        return (t_end * 1.0 + (T - t_end) * g) / T if solved(r) else 1.0
    area, t_prev, g_prev = 0.0, 0.0, 1.0
    for t, d, p in traj:
        t = min(t, T)
        area += g_prev * max(0.0, t - t_prev)
        t_prev, g_prev = t, gap_value(d, p)
    if solved(r):
        g_prev = 0.0 if gap_value(r.get("dual_bound"), r.get("primal_bound")) < 1e-4 else g_prev
    area += g_prev * max(0.0, T - t_prev)
    return area / T


def gap_pct(r: dict) -> float:
    return 100.0 * gap_value(r.get("dual_bound"), r.get("primal_bound"))


def feasible(r: dict) -> bool:
    p = r.get("primal_bound")
    return p is not None and math.isfinite(p)


def crashed(r: dict) -> bool:
    return (r.get("rc") not in (0, 1, None) or bool(r.get("harness_timeout"))) and not r.get("load_timeout")


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("dir")
    ap.add_argument("--control", default="dev")
    ap.add_argument("--md")
    ap.add_argument("--boot", type=int, default=5000)
    a = ap.parse_args()
    ref = load_solu()
    runs = [json.loads(p.read_text()) for p in Path(a.dir).glob("*.json")
            if not p.name.startswith("RESOURCES") and not p.name.endswith(".stale.json")]
    by = defaultdict(dict)
    for r in runs:
        by[(r["instance"], r["seed"])][r["arm"]] = r
    arms = sorted({r["arm"] for r in runs} - {a.control})
    no_traj = sum(1 for r in runs if not r.get("trajectory"))
    # a MIP that ran for more than a few seconds always logs progress rows; none means the parser missed them
    parse_fail = [r for r in runs if not r.get("trajectory") and r.get("solver_time", 0) > 5 and not crashed(r)]
    if parse_fail:
        raise SystemExit(f"parser failure: {len(parse_fail)} runs >5 s without a trajectory, e.g. "
                         f"{parse_fail[0]['arm']} {parse_fail[0]['instance']} s{parse_fail[0]['seed']}")
    out = [f"# Hard-set comparison `{a.dir}` (control `{a.control}`)", "",
           f"{len(runs)} runs; {no_traj} without a logged trajectory (PDGI from final bounds).", "",
           "| arm | pairs (inst) | PDGI arm / ctl | ΔPDGI [95% CI, instance bootstrap] | solved (ctl) | feasible (ctl) | "
           "mean final gap % (ctl) | overrun mean/max s (ctl max) | wrong | crashed | ref coverage |",
           "|---" * 11 + "|"]
    details = []
    for arm in arms:
        per_inst = defaultdict(list)  # instance -> [(pdgi_arm, pdgi_ctl)]
        P = []
        for (inst, seed), d in by.items():
            if arm in d and a.control in d:
                x, y = d[arm], d[a.control]
                P.append((x, y))
                per_inst[inst].append((pdgi(x), pdgi(y)))
        if not P:
            continue
        insts = sorted(per_inst)
        diffs = [sum(u - v for u, v in per_inst[i]) / len(per_inst[i]) for i in insts]
        mx = sum(sum(u for u, _ in per_inst[i]) / len(per_inst[i]) for i in insts) / len(insts)
        my = sum(sum(v for _, v in per_inst[i]) / len(per_inst[i]) for i in insts) / len(insts)
        rng = random.Random(0)
        boots = sorted(sum(diffs[rng.randrange(len(diffs))] for _ in diffs) / len(diffs) for _ in range(a.boot))
        lo, hi = boots[int(0.025 * a.boot)], boots[int(0.975 * a.boot) - 1]
        wr = [x for x, _ in P if wrong(x, ref)]
        cr = [x for x, _ in P if crashed(x)]
        cov = sum(1 for x, _ in P if x["instance"] in ref)
        ovx = [x["overrun"] for x, _ in P if not solved(x)]
        ovy = [y["overrun"] for _, y in P if not solved(y)]
        out.append(f"| {arm} | {len(P)} ({len(insts)}) | {mx:.4f} / {my:.4f} | {mx - my:+.4f} [{lo:+.4f}, {hi:+.4f}] | "
                   f"{sum(solved(x) for x, _ in P)} ({sum(solved(y) for _, y in P)}) | "
                   f"{sum(feasible(x) for x, _ in P)} ({sum(feasible(y) for _, y in P)}) | "
                   f"{sum(gap_pct(x) for x, _ in P) / len(P):.1f} ({sum(gap_pct(y) for _, y in P) / len(P):.1f}) | "
                   f"{sum(ovx) / max(1, len(ovx)):.1f}/{max(ovx, default=0):.1f} ({max(ovy, default=0):.1f}) | "
                   f"{len(wr)} | {len(cr)} | {cov}/{len(P)} |")
        for i, df in sorted(zip(insts, diffs), key=lambda t: t[1]):
            if abs(df) >= 0.05:
                details.append(f"| {arm} | {i} | {df:+.3f} |")
        for x in wr + cr:
            details.append(f"| {arm} | {x['instance']} s{x['seed']} | {'WRONG ' + str(wrong(x, ref)) if x in wr else 'CRASH rc=' + str(x.get('rc'))} |")
    out += ["", "PDGI: normalised primal-dual gap integral over the fixed horizon (0 best, 1 = no usable bounds "
            "throughout). ΔPDGI < 0 favours the arm; the CI resamples instances with their seeds kept together.", ""]
    if details:
        out += ["## Instances with |ΔPDGI| ≥ 0.05 (seed mean), wrong answers, crashes", "",
                "| arm | instance | ΔPDGI / note |", "|---|---|---|"] + details
    text = "\n".join(out)
    print(text)
    if a.md:
        Path(a.md).write_text(text + "\n")


if __name__ == "__main__":
    main()
