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

**Evidence so far:** static read of `latest` on 2026-09-25 (checked by hand).
Profile share: not measured yet.

## Log
- 2026-09-25 filed from the codebase sweep.
