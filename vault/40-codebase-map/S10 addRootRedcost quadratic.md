---
id: S10
area: mip
status: candidate
gate: identical
effort: 2-4 h
verified_in_source: false
profiled_share: null
branch: null
---
# S10: addRootRedcost quadratic

**Where:** highs/mip/HighsRedcostFixing.cpp:266-287

**What:** O(steps x map) multimap walks per column per root resolve.

**Proposed fix:** Pareto staircase in a sorted vector.

**Source:** static read of `latest` on 2026-09-25 (sweep agent, not yet checked by hand).
Measured share, branch and status: see frontmatter (kept current there only).

## Log
- 2026-09-25 filed from the codebase sweep.
