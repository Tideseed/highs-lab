---
id: S11
area: mip
status: candidate
gate: identical
effort: <1 h
verified_in_source: false
profiled_share: null
branch: null
---
# S11: Small per-call allocations

**Where:** highs/mip/HighsCutPool.cpp:23, 643; HighsRedcostFixing.cpp:90

**What:** Per-call vectors in cut hashing, pool sync, redcost reserve.

**Proposed fix:** Member buffers.

**Evidence so far:** static read of `latest` on 2026-09-25 (sweep agent, not yet checked by hand).
Profile share: not measured yet.

## Log
- 2026-09-25 filed from the codebase sweep.
