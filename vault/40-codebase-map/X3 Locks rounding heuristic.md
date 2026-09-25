---
id: X3
area: mip
status: candidate
gate: full
effort: 1 d
verified_in_source: false
profiled_share: null
branch: null
---
# X3: Locks rounding heuristic

**Where:** highs/mip/HighsPrimalHeuristics.cpp (missing; HiGHS has randomized rounding, ZI round off, shifting off)

**What:** SCIP locks heuristic (fix by lock counts, propagate, solve LP on the rest) found the best solution on 5/12 SCIP-win instances.

**Proposed fix:** Root heuristic: fix variables by down/up-lock dominance with propagation, then LP + rounding.

**Source:** static read of `latest` on 2026-09-25 (sweep agent, not yet checked by hand).
Measured share, branch and status: see frontmatter (kept current there only).

## Log
- 2026-09-25 filed from the codebase sweep.
