#!/usr/bin/env python3
"""Hard-instance comparison at a fixed time limit (instances rarely solve, so time-to-solve is uninformative).

  bench/hard.py <result-dir> [--control dev] [--md out.md]

Per arm vs control, over instance+seed pairs:
  - solved count, instances with a feasible solution (finite primal bound)
  - primal-dual integral (HiGHS 'P-D integral'): geometric-mean ratio (shift 1) — lower is better
  - final gap: mean of min(gap,100) — lower is better
  - work done in the same time: geometric-mean ratio of LP iterations (shift 100) and nodes (shift 1)
  - overrun past the limit: mean / max
  - wrong answers (bounds vs solu.txt) and crashes — any is a FAIL
  - per-instance lines where the arm differs strongly (PDI ratio < 0.8 or > 1.25, or solution found by one only)
"""
from __future__ import annotations

import argparse
import json
import math
from collections import defaultdict
from pathlib import Path

from analyze import load_solu, solved, wrong


def gap_of(r: dict) -> float:
    g = r.get("gap", "")
    try:
        return min(100.0, float(str(g).split("%")[0]))
    except ValueError:
        return 100.0


def feasible(r: dict) -> bool:
    p = r.get("primal_bound")
    return p is not None and math.isfinite(p)


def gm_ratio(a: list[float], b: list[float], shift: float) -> float:
    if not a:
        return float("nan")
    return math.exp(sum(math.log((x + shift) / (y + shift)) for x, y in zip(a, b)) / len(a))


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("dir")
    ap.add_argument("--control", default="dev")
    ap.add_argument("--md")
    a = ap.parse_args()
    ref = load_solu()
    runs = [json.loads(p.read_text()) for p in Path(a.dir).glob("*.json") if not p.name.startswith("RESOURCES")]
    by = defaultdict(dict)
    for r in runs:
        by[(r["instance"], r["seed"])][r["arm"]] = r
    arms = sorted({r["arm"] for r in runs} - {a.control})
    out = [f"# Hard-set comparison `{a.dir}` (control `{a.control}`)", "",
           "| arm | pairs | solved (ctl) | feasible (ctl) | PDI ratio | mean gap (ctl) | LP iters ratio | nodes ratio | "
           "mean/max overrun (ctl max) | wrong | crashed |", "|---" * 11 + "|"]
    details = []
    for arm in arms:
        P = [(d[arm], d[a.control]) for d in by.values() if arm in d and a.control in d]
        if not P:
            continue
        ok = [(x, y) for x, y in P if x.get("pd_integral") is not None and y.get("pd_integral") is not None]
        pdi = gm_ratio([x["pd_integral"] for x, _ in ok], [y["pd_integral"] for _, y in ok], 1.0)
        lpi = gm_ratio([x.get("lp_iterations", 0) for x, _ in P], [y.get("lp_iterations", 0) for _, y in P], 100)
        nod = gm_ratio([x.get("nodes", 0) for x, _ in P], [y.get("nodes", 0) for _, y in P], 1)
        wr = [x for x, _ in P if wrong(x, ref)]
        cr = [x for x, _ in P if x.get("rc") not in (0, 1, None) or x.get("harness_timeout")]
        ovx = [x["overrun"] for x, _ in P if not solved(x)]
        ovy = [y["overrun"] for _, y in P if not solved(y)]
        out.append(f"| {arm} | {len(P)} | {sum(solved(x) for x, _ in P)} ({sum(solved(y) for _, y in P)}) | "
                   f"{sum(feasible(x) for x, _ in P)} ({sum(feasible(y) for _, y in P)}) | {pdi:.3f} | "
                   f"{sum(gap_of(x) for x, _ in P) / len(P):.1f} ({sum(gap_of(y) for _, y in P) / len(P):.1f}) | "
                   f"{lpi:.3f} | {nod:.3f} | {sum(ovx) / max(1, len(ovx)):.1f}/{max(ovx, default=0):.1f} "
                   f"({max(ovy, default=0):.1f}) | {len(wr)} | {len(cr)} |")
        for x, y in sorted(P, key=lambda t: t[0]["instance"]):
            px, py = x.get("pd_integral"), y.get("pd_integral")
            flag = feasible(x) != feasible(y) or (px is not None and py is not None and
                                                   not 0.8 <= (px + 1) / (py + 1) <= 1.25)
            if flag or wrong(x, ref) or x in cr:
                details.append(f"| {arm} | {x['instance']} | {py} → {px} | {gap_of(y):.1f} → {gap_of(x):.1f} | "
                               f"{y.get('lp_iterations')} → {x.get('lp_iterations')} | {y['overrun']:.1f} → "
                               f"{x['overrun']:.1f} | {wrong(x, ref) or ''}{' CRASH rc=' + str(x.get('rc')) if x in cr else ''} |")
    out += ["", "PDI / LP-iteration / node ratios are geometric means of arm/control (PDI below 1 = better; "
            "iterations above 1 = more work done in the same time).", ""]
    if details:
        out += ["## Instances that differ strongly", "", "| arm | instance | PDI | gap % | LP iters | overrun s | note |",
                "|---|---|---|---|---|---|---|"] + details
    text = "\n".join(out)
    print(text)
    if a.md:
        Path(a.md).write_text(text + "\n")


if __name__ == "__main__":
    main()
