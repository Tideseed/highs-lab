#!/usr/bin/env python3
"""Independent feasibility check of a HiGHS solution file against the ORIGINAL model (rows, bounds, integrality,
objective recomputed from scratch). solcheck.py <model.mps.gz> <solution.sol> [tol=1e-6]"""
import sys, re
import numpy as np
import highspy
model, sol = sys.argv[1], sys.argv[2]
tol = float(sys.argv[3]) if len(sys.argv) > 3 else 1e-6
h = highspy.Highs(); h.setOptionValue("output_flag", False); h.readModel(model)
lp = h.getLp()
names = list(lp.col_names_) if lp.num_col_ else None  # copy once: indexing the pybind vector copies it
vals = {}
txt = open(sol).read()
m = re.search(r"# Columns (\d+)\n(.*?)\n# Rows", txt, re.S)
for line in m.group(2).splitlines():
    k, v = line.rsplit(None, 1); vals[k] = float(v)
x = np.array([vals[names[j]] for j in range(lp.num_col_)])
A = lp.a_matrix_; start = np.array(A.start_); idx = np.array(A.index_); val = np.array(A.value_)
act = np.zeros(lp.num_row_)
for j in range(lp.num_col_):
    act[idx[start[j]:start[j+1]]] += val[start[j]:start[j+1]] * x[j]
lo, up = np.array(lp.row_lower_), np.array(lp.row_upper_)
# row-local scaling: a row's allowed residual scales with that row's own magnitude (max |a_ij x_j| and |rhs|),
# never with the largest activity anywhere in the model
absact = np.zeros(lp.num_row_)
for j in range(lp.num_col_):
    absact[idx[start[j]:start[j+1]]] = np.maximum(absact[idx[start[j]:start[j+1]]],
                                                  np.abs(val[start[j]:start[j+1]] * x[j]))
rhsmag = np.maximum(np.where(np.isfinite(lo), np.abs(lo), 0), np.where(np.isfinite(up), np.abs(up), 0))
rowscale = np.maximum(1.0, np.maximum(absact, rhsmag))
rowviol = np.maximum(np.where(np.isfinite(lo), lo - act, 0), np.where(np.isfinite(up), act - up, 0))
rel_row = np.max(np.maximum(rowviol, 0) / rowscale, initial=0)
viol_row = np.max(np.maximum(rowviol, 0), initial=0)
cl, cu = np.array(lp.col_lower_), np.array(lp.col_upper_)
viol_bnd = max(np.max(np.where(np.isfinite(cl), cl - x, 0), initial=0), np.max(np.where(np.isfinite(cu), x - cu, 0), initial=0))
integ = np.array([int(t) for t in lp.integrality_]) if len(lp.integrality_) else np.zeros(lp.num_col_)
viol_int = np.max(np.abs(x[integ == 1] - np.round(x[integ == 1])), initial=0)
finite = bool(np.all(np.isfinite(x)))
obj = float(np.dot(np.array(lp.col_cost_), x) + lp.offset_)
ok = finite and rel_row <= tol and viol_bnd <= tol * np.maximum(1, np.max(np.abs(x), initial=1)) and viol_int <= 1e-5
print(f"{'FEASIBLE' if ok else 'INFEASIBLE'} obj={obj:.9g} maxrow_abs={viol_row:.2e} maxrow_rel={rel_row:.2e} maxbound={viol_bnd:.2e} maxint={viol_int:.2e} finite={finite}")
sys.exit(0 if ok else 1)
