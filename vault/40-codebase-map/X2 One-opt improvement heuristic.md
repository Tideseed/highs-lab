---
id: X2
area: mip
status: candidate
gate: full
effort: 0.5-1 d
verified_in_source: false
profiled_share: null
branch: null
---
# X2: One-opt improvement heuristic

**Where:** highs/mip/HighsPrimalHeuristics.cpp (missing)

**What:** SCIP oneopt found the best solution on 3/12 SCIP-win instances (neos-787933, rail507, ...). Shift one variable at a time in the objective-improving direction as far as rows allow, after each new incumbent.

**Proposed fix:** New heuristic after incumbent updates; cheap O(nnz).

**Source:** static read of `latest` on 2026-09-25 (sweep agent, not yet checked by hand).
Measured share, branch and status: see frontmatter (kept current there only).

## Log
- 2026-09-25 filed from the codebase sweep.
