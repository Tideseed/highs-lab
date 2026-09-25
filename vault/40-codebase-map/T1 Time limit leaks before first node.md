---
id: T1
area: mip
status: explained
gate: full + overrun metric
effort: hours
verified_in_source: false
profiled_share: null
branch: null
---
# T1: Time limit leaks before first node

**Where:** highs/mip/HighsMipSolverData.cpp ~445 (analytic-centre IPM options), ~501 finishAnalyticCenterComputation sync, 2148/2514 tg.cancel()+taskWait, ~TaskGroup on early returns; highs/parallel/HighsParallel.h:97 cancel() only cancels unstarted tasks; HighsSymmetry.cpp:1666 run() no deadline; HighsFeasibilityJump.cpp:107 effort-only stop

**What:** Upstream #3314 (ours): s100 with time_limit=60 ran 240-400 s with 0 nodes. Suspected: the analytic-centre IPM has no time limit and the root waits on it even after detecting the time limit.

**Proposed fix:** Pass remaining time to the IPM; checkLimits before syncs; timer check in the FJ callback; deadline/stop flag in symmetry detection.

**Source:** static read of `latest` on 2026-09-25 (sweep agent, not yet checked by hand).
Measured share, branch and status: see frontmatter (kept current there only).

## Log
- 2026-09-25 filed from the codebase sweep.
- 2026-09-25 perf on s100 (dev 6293630a84): the overrun is NOT the analytic-centre IPM; 90 % of the run is setupCliquePartition → see [[C1 Clique partition pairwise queries]]. Remaining T1 idea: a time check after setupCliquePartition / in runSetup, so no other setup phase can overrun.
