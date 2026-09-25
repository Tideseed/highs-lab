---
id: P9
area: presolve
status: candidate
gate: n/a
effort: trivial
verified_in_source: true
profiled_share: null
branch: null
---
# P9: Debug printf in presolve

**Where:** highs/presolve/HPresolve.cpp:8644, 6696

**What:** Leftover printf when num_reductions == 35044 fires in production.

**Proposed fix:** Delete (report only).

**Source:** static read of `latest` on 2026-09-25 (checked by hand).
Measured share, branch and status: see frontmatter (kept current there only).

## Log
- 2026-09-25 filed from the codebase sweep.
