#!/usr/bin/env python3
"""Compare arms of a bench/run.py result directory against a control arm.

  bench/analyze.py bench/results/raw/<run-id> --control dev [--identical] [--md out.md]

Metrics (per arm vs control, seeds averaged per instance first):
  - shifted geometric mean of solve time, shift 10 s, unsolved counted at the limit (all instances) and on
    instances solved by both; ratio arm/control with a paired bootstrap 95 % CI over instances
  - solved count, mean overrun past the time limit, max overrun
  - wrong answers: a reported bound pair that excludes the known optimum (solu.txt), or 'Optimal' with an
    objective outside tolerance. Any wrong answer fails the gate.
  - --identical: for instance+seed runs that both arms solved, node count, LP iterations and objective must be
    equal (for branches that claim to be pure speed-ups)
Gate: time ratio <= 0.97 with CI upper bound < 1, no wrong answers, solved count not lower.
"""
from __future__ import annotations

import argparse
import json
import math
import random
from collections import defaultdict
from pathlib import Path

SOLU = Path("~/data/optopt/miplib/solu.txt").expanduser()
SHIFT = 10.0


def load_solu() -> dict[str, float]:
    ref = {}
    if SOLU.exists():
        for line in SOLU.read_text().splitlines():
            p = line.split()
            if len(p) >= 3 and p[0] in ("=opt=", "=best="):
                try:
                    ref[p[1]] = (float(p[2]), p[0] == "=opt=")
                except ValueError:
                    pass
    return ref


def solved(r: dict) -> bool:
    return r.get("status") == "Optimal" or r.get("lp_status") == "Optimal"


def time_of(r: dict) -> float:
    t = r.get("solver_time", r.get("lp_time", r["wall"]))
    return t if solved(r) else max(r["time_limit"], t)


def sgm(xs: list[float]) -> float:
    return math.exp(sum(math.log(x + SHIFT) for x in xs) / len(xs)) - SHIFT


def wrong(r: dict, ref: dict) -> str | None:
    if r["instance"] not in ref:
        return None
    opt, is_opt = ref[r["instance"]]
    tol = 1e-6 + 1e-4 * max(1.0, abs(opt))
    p, d = r.get("primal_bound"), r.get("dual_bound")
    if is_opt and p is not None and d is not None and all(map(math.isfinite, (p, d))):
        lo, hi = min(p, d), max(p, d)
        if not (lo - tol <= opt <= hi + tol):
            return f"bounds [{lo}, {hi}] exclude optimum {opt}"
    if is_opt and solved(r) and p is not None and abs(p - opt) > tol:
        return f"Optimal with {p}, optimum {opt}"
    return None


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("dir")
    ap.add_argument("--control", default="dev")
    ap.add_argument("--identical", action="store_true")
    ap.add_argument("--md")
    ap.add_argument("--boot", type=int, default=5000)
    a = ap.parse_args()

    ref = load_solu()
    runs = [json.loads(p.read_text()) for p in Path(a.dir).glob("*.json")
            if not p.name.startswith("RESOURCES") and not p.name.endswith(".stale.json")]
    by = defaultdict(dict)  # (instance, seed) -> arm -> rec
    for r in runs:
        by[(r["instance"], r["seed"])][r["arm"]] = r
    arms = sorted({r["arm"] for r in runs})
    lines = [f"# Bench analysis: `{a.dir}`", "", f"control = `{a.control}`, {len(runs)} runs, arms: {', '.join(arms)}", ""]

    wrongs = [(r["arm"], r["instance"], r["seed"], w) for r in runs if (w := wrong(r, ref))]
    # rc 1 is HiGHS's warning status (e.g. time limit reached); anything else non-zero is a crash
    fails = [r for r in runs if (r.get("rc") not in (0, 1, None) or r.get("harness_timeout"))
             and not r.get("load_timeout")]
    load_timeouts = [r for r in runs if r.get("load_timeout")]
    identical_diffs: dict = {}
    if a.identical:
        for arm in arms:
            if arm == a.control:
                continue
            n, diffs = 0, []
            for (inst, seed), d in sorted(by.items()):
                if arm in d and a.control in d and solved(d[arm]) and solved(d[a.control]):
                    n += 1
                    x, y = d[arm], d[a.control]
                    keys = ("nodes", "lp_iterations", "primal_bound", "simplex_iterations", "objective")
                    dk = [k for k in keys if x.get(k) != y.get(k)]
                    if dk:
                        diffs.append(f"- {inst} s{seed}: " + ", ".join(f"{k} {y.get(k)}->{x.get(k)}" for k in dk))
            identical_diffs[arm] = (n, diffs)

    lines += ["| arm | n inst | solved | SGM all (s) | ratio vs control [95% CI] | SGM both-solved | ratio | "
              "mean overrun (s) | max overrun (s) | wrong | crashed |", "|---" * 11 + "|"]
    verdicts = {}
    for arm in arms:
        pairs = defaultdict(lambda: ([], [], [], []))  # instance -> (t_arm, t_ctl, solved_arm, solved_ctl)
        for (inst, seed), d in by.items():
            if arm in d and a.control in d:
                pa, pc = d[arm], d[a.control]
                pairs[inst][0].append(time_of(pa)); pairs[inst][1].append(time_of(pc))
                pairs[inst][2].append(solved(pa)); pairs[inst][3].append(solved(pc))
        insts = sorted(pairs)
        if not insts:
            continue
        ta = [sum(pairs[i][0]) / len(pairs[i][0]) for i in insts]
        tc = [sum(pairs[i][1]) / len(pairs[i][1]) for i in insts]
        both = [k for k, i in enumerate(insts) if all(pairs[i][2]) and all(pairs[i][3])]
        ratio = sgm(ta) / sgm(tc)
        rng = random.Random(0)
        boots = []
        for _ in range(a.boot if arm != a.control else 0):
            idx = [rng.randrange(len(insts)) for _ in insts]
            boots.append(sgm([ta[k] for k in idx]) / sgm([tc[k] for k in idx]))
        boots.sort()
        ci = (boots[int(0.025 * len(boots))], boots[int(0.975 * len(boots)) - 1]) if boots else (1, 1)
        rb = (sgm([ta[k] for k in both]) / sgm([tc[k] for k in both])) if both else float("nan")
        arm_runs = [r for r in runs if r["arm"] == arm]
        # solved counts on the paired set only
        paired = [(d[arm], d[a.control]) for d in by.values() if arm in d and a.control in d]
        n_solved = sum(solved(x) for x, _ in paired)
        ctl_solved = sum(solved(y) for _, y in paired)
        ov = [r["overrun"] for r in arm_runs if not solved(r)]
        nw = sum(1 for w in wrongs if w[0] == arm)
        nf = sum(1 for r in fails if r["arm"] == arm)
        lines.append(f"| {arm} | {len(insts)} | {n_solved} | {sgm(ta):.2f} | {ratio:.3f} [{ci[0]:.3f}, {ci[1]:.3f}] | "
                     f"{sgm([ta[k] for k in both]) if both else float('nan'):.2f} | {rb:.3f} | "
                     f"{(sum(ov) / len(ov)) if ov else 0:.1f} | {max(ov) if ov else 0:.1f} | {nw} | {nf} |")
        if arm != a.control:
            reasons = []
            if not (ratio <= 0.97 and ci[1] < 1):
                reasons.append("speed")
            if nw:
                reasons.append(f"{nw} wrong")
            if nf:
                reasons.append(f"{nf} crashed")
            if n_solved < ctl_solved:
                reasons.append("fewer solved")
            if a.identical and identical_diffs.get(arm, (0, []))[1]:
                reasons.append(f"search differs on {len(identical_diffs[arm][1])}")
            verdicts[arm] = "PASS" if not reasons else "no pass (" + ", ".join(reasons) + ")"
    cov_opt = sum(1 for r in runs if r["instance"] in ref and ref[r["instance"]][1])
    cov_best = sum(1 for r in runs if r["instance"] in ref and not ref[r["instance"]][1])
    cov = cov_opt
    if load_timeouts:
        lines += ["", f"Load timeouts (model not read within the limit, not counted as crashes): "
                  + ", ".join(sorted({f"{r['arm']}:{r['instance']}" for r in load_timeouts}))]
    served = sum(1 for r in runs if "active" in (r.get("serving_units") or {}).values())
    unknown = sum(1 for r in runs if "serving_units" not in r)
    lines += ["", f"Contention: {served}/{len(runs)} runs ended with a local LLM server active"
              + (f" ({unknown} runs predate per-job recording)" if unknown else "") + "."]
    lines += ["", "Gate (ratio <= 0.97, CI upper < 1, no wrong answers, no crashes, solved >= control on paired runs"
              + (", identical search" if a.identical else "") + "): " +
              ", ".join(f"{k} {v}" for k, v in verdicts.items()), "",
              f"Reference coverage: {cov_opt}/{len(runs)} runs have a KNOWN OPTIMUM (=opt=, checked: bounds must "
              f"bracket it, 'Optimal' must match it); {cov_best} have only a best-known value (=best=, not checked); "
              f"{len(runs) - cov_opt - cov_best} have no reference. Unchecked runs are not evidence of correctness. "
              "Objective checks do not establish primal feasibility (see bench/solcheck.py).",
              "Instances without a known optimum: " + ", ".join(sorted({r['instance'] for r in runs
                                                                         if not (r['instance'] in ref and ref[r['instance']][1])})), ""]

    if wrongs:
        lines += ["## Wrong answers", ""] + [f"- {a_} {i} s{s}: {w}" for a_, i, s, w in wrongs] + [""]
    if fails:
        lines += ["## Crashes / harness timeouts", ""] + [f"- {r['arm']} {r['instance']} s{r['seed']} rc={r.get('rc')}"
                                                         f" timeout={r.get('harness_timeout')}" for r in fails] + [""]
    if a.identical:
        lines += ["## Identical-search check (both solved)", ""]
        for arm, (n, diffs) in identical_diffs.items():
            lines.append(f"**{arm}**: {n - len(diffs)}/{n} identical")
            lines += diffs + [""]
    text = "\n".join(lines)
    print(text)
    if a.md:
        Path(a.md).write_text(text + "\n")


if __name__ == "__main__":
    main()
