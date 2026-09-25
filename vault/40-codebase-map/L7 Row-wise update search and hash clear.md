---
id: L7
area: util
status: candidate
gate: identical
effort: 0.5-1 d
verified_in_source: false
profiled_share: null
branch: null
---
# L7: Row-wise update search and hash clear

**Where:** highs/util/HighsSparseMatrix.cpp:1586; HighsHash.h:1135

**What:** Linear search per row update on basis change; hash clear() shrinks to 128 slots.

**Proposed fix:** Position map; clear() keeps capacity.

**Source:** static read of `latest` on 2026-09-25 (sweep agent, not yet checked by hand).
Measured share, branch and status: see frontmatter (kept current there only).

## Log
- 2026-09-25 filed from the codebase sweep.
