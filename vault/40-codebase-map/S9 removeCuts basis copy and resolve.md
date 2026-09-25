---
id: S9
area: mip
status: candidate
gate: full
effort: 0.5 d
verified_in_source: false
profiled_share: null
branch: null
---
# S9: removeCuts basis copy and resolve

**Where:** highs/mip/HighsLpRelaxation.cpp:587-607

**What:** Basis copied and optimizeLp called right after deleting rows.

**Proposed fix:** Edit basis in place; defer re-solve.

**Source:** static read of `latest` on 2026-09-25 (sweep agent, not yet checked by hand).
Measured share, branch and status: see frontmatter (kept current there only).

## Log
- 2026-09-25 filed from the codebase sweep.
