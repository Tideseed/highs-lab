#!/usr/bin/env python3
"""Quick screen: find out FAST whether a candidate arm is worth more time. Fails early.

  bench/screen.py --arm <name> [--control dev] [--identical] [--set bench/sets/quick.txt] [--time-limit 60]

Runs the instances in waves of --wave (default 10 = one per X925 core), seed 0, arm and control side by side.
After every wave it stops with FAIL as soon as:
  - any wrong answer or crash in the arm, or
  - --identical and any both-solved run differs in nodes / LP iterations (pure speed-up claim broken), or
  - the running time ratio (shifted geomean, arm/control) is above --kill (default 1.02)
It stops with PROMISING when the ratio is below --promote (default 0.95) after at least --min-waves waves, and
otherwise continues until the set is exhausted (verdict NEUTRAL or PROMISING). PROMISING means "worth a full gate
run", not a result.
"""
from __future__ import annotations

import argparse
import json
import math
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
from analyze import load_solu, sgm, solved, time_of, wrong  # noqa: E402


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--arm", required=True)
    ap.add_argument("--control", default="dev")
    ap.add_argument("--arms", default=str(HERE / "arms.toml"))
    ap.add_argument("--set", default=str(HERE / "sets/quick.txt"))
    ap.add_argument("--time-limit", type=float, default=60)
    ap.add_argument("--wave", type=int, default=10)
    ap.add_argument("--min-waves", type=int, default=2)
    ap.add_argument("--kill", type=float, default=1.02)
    ap.add_argument("--promote", type=float, default=0.95)
    ap.add_argument("--identical", action="store_true")
    ap.add_argument("--cores", default="5-9,15-19")
    ap.add_argument("--out")
    a = ap.parse_args()

    names = [l.strip() for l in Path(a.set).read_text().splitlines() if l.strip() and not l.startswith("#")]
    out = Path(a.out or HERE / f"results/raw/screen-{a.arm}")
    ref = load_solu()
    verdict = "NEUTRAL"
    reason = "set exhausted"
    for w in range(0, len(names), a.wave):
        wave = names[w:w + a.wave]
        sub = out / f"wave{w // a.wave}.txt"
        out.mkdir(parents=True, exist_ok=True)
        sub.write_text("\n".join(wave) + "\n")
        subprocess.run([sys.executable, str(HERE / "run.py"), "--arms", a.arms, "--only-arms", a.control, a.arm,
                        "--set", str(sub), "--seeds", "0", "--time-limit", str(a.time_limit), "--cores", a.cores,
                        "--out", str(out)], check=True, stdout=subprocess.DEVNULL)
        runs = [json.loads(p.read_text()) for p in out.glob("*.json")
                if not p.name.startswith("RESOURCES") and not p.name.endswith(".stale.json")]
        by: dict = {}
        for r in runs:
            by.setdefault(r["instance"], {})[r["arm"]] = r
        pairs = [(d[a.arm], d[a.control]) for d in by.values() if a.arm in d and a.control in d]
        bad = [f"{x['instance']}: {wrong(x, ref)}" for x, _ in pairs if wrong(x, ref)]
        bad += [f"{x['instance']}: crash rc={x.get('rc')}" for x, _ in pairs
                if x.get("rc") not in (0, 1, None) or x.get("harness_timeout")]
        if a.identical:
            bad += [f"{x['instance']}: search differs (nodes {y.get('nodes')}->{x.get('nodes')}, "
                    f"lp {y.get('lp_iterations')}->{x.get('lp_iterations')})"
                    for x, y in pairs if solved(x) and solved(y)
                    and (x.get("nodes"), x.get("lp_iterations")) != (y.get("nodes"), y.get("lp_iterations"))]
        ratio = sgm([time_of(x) for x, _ in pairs]) / sgm([time_of(y) for _, y in pairs])
        per = sorted(((time_of(x) + 1) / (time_of(y) + 1), x["instance"]) for x, y in pairs)
        print(f"wave {w // a.wave}: n={len(pairs)} ratio={ratio:.3f} best={per[0][1]} {per[0][0]:.2f} "
              f"worst={per[-1][1]} {per[-1][0]:.2f}", flush=True)
        if bad:
            verdict, reason = "FAIL", "; ".join(bad[:5])
            break
        if ratio > a.kill:
            verdict, reason = "FAIL", f"ratio {ratio:.3f} > {a.kill}"
            break
        if ratio < a.promote and (w // a.wave + 1) >= a.min_waves:
            verdict, reason = "PROMISING", f"ratio {ratio:.3f} after {len(pairs)} instances"
            break
        if ratio < a.promote:
            verdict = "PROMISING"
            reason = f"ratio {ratio:.3f}"
    print(f"VERDICT {a.arm}: {verdict} ({reason})")


if __name__ == "__main__":
    main()
