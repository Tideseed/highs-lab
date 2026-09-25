---
id: P6
area: lp_data
status: candidate
gate: identical
effort: 2-4 h
verified_in_source: false
profiled_share: null
branch: null
---
# P6: assessMatrix hash per nonzero

**Where:** highs/util/HighsMatrixUtils.cpp:163+; Highs.cpp:1377

**What:** Duplicate check hashes every nonzero on every passModel incl. internal MIP reloads and per-worker copies.

**Proposed fix:** Stamp array; skip for internal calls.

**Source:** static read of `latest` on 2026-09-25 (sweep agent, not yet checked by hand).
Measured share, branch and status: see frontmatter (kept current there only).

## Log
- 2026-09-25 filed from the codebase sweep.
