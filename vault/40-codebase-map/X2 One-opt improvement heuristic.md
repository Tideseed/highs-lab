---
id: X2
area: mip
status: parked
gate: full
effort: 0.5-1 d
verified_in_source: false
profiled_share: null
branch: lab/one-opt
---
# X2: One-opt improvement heuristic

**Where:** highs/mip/HighsPrimalHeuristics.cpp (missing)

**What:** SCIP oneopt found the best solution on 3/12 SCIP-win instances (neos-787933, rail507, ...). Shift one variable at a time in the objective-improving direction as far as rows allow, after each new incumbent.

**Proposed fix:** New heuristic after incumbent updates; cheap O(nnz).

**Source:** static read of `latest` on 2026-09-25 (sweep agent, not yet checked by hand).
Measured share, branch and status: see frontmatter (kept current there only).

## Log
- 2026-09-25 filed from the codebase sweep.
- 2026-09-25 evening: implemented (lab/one-opt, 70 lines, called after each improving incumbent; 101/101 tests). First screen (5 primal-weak instances, 60 s, A725): one-opt never produced a solution (no H rows); only side effects via changed paths. Parked; diagnose (count candidates/shifts) before any further time.
