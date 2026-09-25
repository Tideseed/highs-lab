#!/usr/bin/env python3
"""Run SCIP (pyscipopt) on one instance, single thread, and dump its full statistics.
run_scip.py <instance-name> <time-limit> <outdir>"""
import sys, time
from pathlib import Path
import pyscipopt
name, tl, out = sys.argv[1], float(sys.argv[2]), Path(sys.argv[3])
out.mkdir(parents=True, exist_ok=True)
m = pyscipopt.Model()
m.hideOutput()
m.readProblem(str(Path.home() / f"data/optopt/miplib/inst/{name}.mps.gz"))
m.setParam("limits/time", tl)
m.setParam("parallel/maxnthreads", 1)
m.setParam("randomization/randomseedshift", 0)
t = time.time(); m.optimize(); wall = time.time() - t
m.writeStatistics(str(out / f"{name}.stats"))
(out / f"{name}.summary").write_text(f"{name} status={m.getStatus()} wall={wall:.1f} primal={m.getPrimalbound()} dual={m.getDualbound()} nodes={m.getNNodes()}\n")
print((out / f"{name}.summary").read_text(), end="")
