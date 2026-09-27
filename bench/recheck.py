#!/usr/bin/env python3
"""Re-check every saved solution of a result dir with solcheck.check (local tolerances) and report coverage.

  <venv with numpy+highspy>/bin/python bench/recheck.py <result-dir> [--md out.md]

Coverage is reported separately: runs, runs with a finite final primal bound, saved solution files, parsed and checked,
FEASIBLE / INFEASIBLE. A missing or unparsable solution file is a coverage gap, never counted as feasible. Loads one
model at a time (a model is read once for all its runs); run it outside a benchmark window, under a memory cap.
"""
from __future__ import annotations

import argparse
import json
import math
import re
from collections import defaultdict
from pathlib import Path

import numpy as np
import highspy

from solcheck import check

INST = Path("~/data/optopt/miplib/inst").expanduser()


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("dir")
    ap.add_argument("--md")
    a = ap.parse_args()
    d = Path(a.dir)
    runs = [json.loads(p.read_text()) for p in d.glob("*.json")
            if not p.name.startswith("RESOURCES") and not p.name.endswith(".stale.json")]
    by_inst = defaultdict(list)
    for r in runs:
        by_inst[r["instance"]].append(r)
    cnt = defaultdict(int)
    bad, worst = [], []
    for inst in sorted(by_inst):
        todo = []
        for r in by_inst[inst]:
            cnt["runs"] += 1
            if r.get("primal_bound") is None or not math.isfinite(r["primal_bound"]):
                continue
            cnt["with_incumbent"] += 1
            sol = d / "work" / f"{r['arm']}__{inst}__s{r['seed']}" / "solution.sol"
            if not sol.exists():
                cnt["no_file"] += 1
                continue
            todo.append((r, sol))
        if not todo:
            continue
        h = highspy.Highs(); h.setOptionValue("output_flag", False); h.readModel(str(INST / f"{inst}.mps.gz"))
        lp = h.getLp(); A = lp.a_matrix_
        names = list(lp.col_names_)
        rnames = list(lp.row_names_) if len(lp.row_names_) else None
        cols = (list(lp.col_lower_), list(lp.col_upper_), [int(t) for t in lp.integrality_], list(lp.row_lower_),
                list(lp.row_upper_), list(A.start_), list(A.index_), list(A.value_))
        cost, off = np.array(lp.col_cost_), lp.offset_
        for r, sol in todo:
            m = re.search(r"# Columns (\d+)\n(.*?)\n# Rows", sol.read_text(), re.S)
            if not m:
                cnt["unparsable"] += 1
                continue
            vals = dict((k, float(v)) for k, v in (ln.rsplit(None, 1) for ln in m.group(2).splitlines()))
            if any(n not in vals for n in names):
                cnt["unparsable"] += 1
                continue
            x = np.array([vals[n] for n in names])
            c = check(x, *cols, 1e-6, names, rnames)
            cnt["checked"] += 1
            obj = float(cost @ x + off)
            objdev = abs(obj - r["primal_bound"]) / max(1.0, abs(r["primal_bound"]))
            tag = f"{r['arm']} {inst} s{r['seed']}"
            if c["ok"]:
                cnt["feasible"] += 1
            else:
                bad.append(f"- {tag}: row_rel {c['row_rel']:.2e}@{c['row_rel_at']}, bound_rel {c['bound_rel']:.2e}"
                           f"@{c['bound_rel_at']} (abs {c['bound_abs']:.2e}), int {c['int']:.2e}@{c['int_at']}, finite {c['finite']}")
            if objdev > 1e-6:
                cnt["obj_mismatch"] += 1
                bad.append(f"- {tag}: recomputed objective {obj:.10g} vs reported {r['primal_bound']:.10g}")
            worst.append((c["row_rel"], c["bound_rel"], c["int"], tag))
    wr = max(worst, default=(0, 0, 0, "-"), key=lambda w: w[0])
    wb = max(worst, default=(0, 0, 0, "-"), key=lambda w: w[1])
    wi = max(worst, default=(0, 0, 0, "-"), key=lambda w: w[2])
    out = [f"# Saved-solution recheck `{a.dir}` (solcheck with local tolerances, tol 1e-6, int 1e-5)", "",
           f"runs {cnt['runs']}; with a finite final incumbent {cnt['with_incumbent']}; no saved solution file "
           f"{cnt['no_file']}; unparsable {cnt['unparsable']}; **checked {cnt['checked']}: FEASIBLE {cnt['feasible']}, "
           f"INFEASIBLE {cnt['checked'] - cnt['feasible']}**; objective mismatches {cnt['obj_mismatch']}.", "",
           f"Worst normalised row violation {wr[0]:.2e} ({wr[3]}); worst normalised bound violation {wb[1]:.2e} ({wb[3]}); "
           f"worst integrality {wi[2]:.2e} ({wi[3]}).", ""]
    if bad:
        out += ["## Failures", ""] + bad
    text = "\n".join(out)
    print(text)
    if a.md:
        Path(a.md).write_text(text + "\n")


if __name__ == "__main__":
    main()
