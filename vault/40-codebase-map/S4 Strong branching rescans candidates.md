---
id: S4
area: mip
status: candidate
gate: identical if tie-breaks kept
effort: 0.5 d
verified_in_source: false
profiled_share: null
branch: null
---
# S4: Strong branching rescans candidates

**Where:** highs/mip/HighsSearch.cpp:340-389 selectBestScore, 418-530 analyzeSolution

**What:** O(numfrac^2) per node; getScore touches ~10 per-column arrays.

**Proposed fix:** Heap of scores; pack pseudocost fields; reusable buffers.

**Source:** static read of `latest` on 2026-09-25 (sweep agent, not yet checked by hand).
Measured share, branch and status: see frontmatter (kept current there only).

## Log
- 2026-09-25 filed from the codebase sweep.
