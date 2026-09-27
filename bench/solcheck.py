#!/usr/bin/env python3
"""Independent feasibility check of a HiGHS solution file against the ORIGINAL model (rows, bounds, integrality,
objective recomputed from scratch). solcheck.py <model.mps.gz> <solution.sol> [tol=1e-6]

Every tolerance is LOCAL (review #5, Codex 2026-09-27): a row's residual is scaled by that row's own magnitude
(max |a_ij x_j| and |rhs|); a variable's bound violation by that bound's own magnitude, max(1, |bound|) — never by the
largest value anywhere in the solution; integrality is an absolute distance (1e-5). The worst absolute and normalised
violation of each kind is reported with the offending row/column name.
"""
from __future__ import annotations

import re
import sys

import numpy as np

INT_TOL = 1e-5


def check(x, col_lower, col_upper, integrality, row_lower, row_upper, start, index, value, tol=1e-6,
          col_names=None, row_names=None) -> dict:
    x = np.asarray(x, dtype=float)
    n = len(x)
    cl, cu = np.asarray(col_lower, dtype=float), np.asarray(col_upper, dtype=float)
    lo, up = np.asarray(row_lower, dtype=float), np.asarray(row_upper, dtype=float)
    start, idx, val = np.asarray(start, dtype=np.int64), np.asarray(index, dtype=np.int64), np.asarray(value, dtype=float)
    m = len(lo)
    finite = bool(np.all(np.isfinite(x)))
    act, absact = np.zeros(m), np.zeros(m)
    for j in range(n):
        s, e = start[j], start[j + 1]
        t = val[s:e] * x[j]
        act[idx[s:e]] += t
        absact[idx[s:e]] = np.maximum(absact[idx[s:e]], np.abs(t))
    rhsmag = np.maximum(np.where(np.isfinite(lo), np.abs(lo), 0), np.where(np.isfinite(up), np.abs(up), 0))
    rowscale = np.maximum(1.0, np.maximum(absact, rhsmag))
    rowviol = np.maximum(np.maximum(np.where(np.isfinite(lo), lo - act, 0), np.where(np.isfinite(up), act - up, 0)), 0)
    rowrel = rowviol / rowscale
    # per-variable bound violation, scaled by the violated bound's own magnitude
    vlo = np.where(np.isfinite(cl), np.maximum(cl - x, 0), 0)
    vup = np.where(np.isfinite(cu), np.maximum(x - cu, 0), 0)
    bviol = np.maximum(vlo, vup)
    bscale = np.maximum(1.0, np.where(vlo >= vup, np.where(np.isfinite(cl), np.abs(cl), 0),
                                      np.where(np.isfinite(cu), np.abs(cu), 0)))
    brel = bviol / bscale
    integ = np.asarray(integrality, dtype=int) if len(integrality) else np.zeros(n, dtype=int)
    iviol = np.where(integ == 1, np.abs(x - np.round(x)), 0) if n else np.zeros(0)

    def worst(v, names):
        if len(v) == 0:
            return 0.0, None
        k = int(np.argmax(v))
        return float(v[k]), (names[k] if names is not None else k)

    r = {"finite": finite}
    r["row_rel"], r["row_rel_at"] = worst(rowrel, row_names)
    r["row_abs"], r["row_abs_at"] = worst(rowviol, row_names)
    r["bound_rel"], r["bound_rel_at"] = worst(brel, col_names)
    r["bound_abs"], r["bound_abs_at"] = worst(bviol, col_names)
    r["int"], r["int_at"] = worst(iviol, col_names)
    r["ok"] = finite and r["row_rel"] <= tol and r["bound_rel"] <= tol and r["int"] <= INT_TOL
    return r


def main() -> None:
    import highspy
    model, sol = sys.argv[1], sys.argv[2]
    tol = float(sys.argv[3]) if len(sys.argv) > 3 else 1e-6
    h = highspy.Highs(); h.setOptionValue("output_flag", False); h.readModel(model)
    lp = h.getLp()
    names = list(lp.col_names_) if lp.num_col_ else None  # copy once: indexing the pybind vector copies it
    rnames = list(lp.row_names_) if lp.num_row_ and len(lp.row_names_) else None
    vals = {}
    m = re.search(r"# Columns (\d+)\n(.*?)\n# Rows", open(sol).read(), re.S)
    for line in m.group(2).splitlines():
        k, v = line.rsplit(None, 1); vals[k] = float(v)
    x = np.array([vals[names[j]] for j in range(lp.num_col_)])
    A = lp.a_matrix_
    r = check(x, lp.col_lower_, lp.col_upper_, [int(t) for t in lp.integrality_], lp.row_lower_, lp.row_upper_,
              A.start_, A.index_, A.value_, tol, names, rnames)
    obj = float(np.dot(np.array(lp.col_cost_), x) + lp.offset_)
    print(f"{'FEASIBLE' if r['ok'] else 'INFEASIBLE'} obj={obj:.9g} "
          f"row_rel={r['row_rel']:.2e}@{r['row_rel_at']} row_abs={r['row_abs']:.2e}@{r['row_abs_at']} "
          f"bound_rel={r['bound_rel']:.2e}@{r['bound_rel_at']} bound_abs={r['bound_abs']:.2e}@{r['bound_abs_at']} "
          f"int={r['int']:.2e}@{r['int_at']} finite={r['finite']}")
    sys.exit(0 if r["ok"] else 1)


if __name__ == "__main__":
    main()
