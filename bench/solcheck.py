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
viol_row = max(np.max(lo - act, initial=0), np.max(act - up, initial=0))
cl, cu = np.array(lp.col_lower_), np.array(lp.col_upper_)
viol_bnd = max(np.max(cl - x, initial=0), np.max(x - cu, initial=0))
integ = np.array([int(t) for t in lp.integrality_]) if len(lp.integrality_) else np.zeros(lp.num_col_)
viol_int = np.max(np.abs(x[integ == 1] - np.round(x[integ == 1])), initial=0)
obj = float(np.dot(np.array(lp.col_cost_), x) + lp.offset_)
ok = viol_row <= tol * max(1, np.max(np.abs(act), initial=1)) and viol_bnd <= tol and viol_int <= 1e-5
print(f"{'FEASIBLE' if ok else 'INFEASIBLE'} obj={obj:.9g} maxrow={viol_row:.2e} maxbound={viol_bnd:.2e} maxint={viol_int:.2e}")
sys.exit(0 if ok else 1)
