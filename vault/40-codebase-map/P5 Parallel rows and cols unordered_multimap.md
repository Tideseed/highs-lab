---
id: P5
area: presolve
status: candidate
gate: identical
effort: 0.5 d
verified_in_source: false
profiled_share: null
branch: null
---
# P5: Parallel rows/cols unordered_multimap

**Where:** highs/presolve/HPresolve.cpp:8997

**What:** ~600k node allocations per call, up to 5 calls.

**Proposed fix:** Sort (hash, idx) vector.

**Evidence so far:** static read of `latest` on 2026-09-25 (sweep agent, not yet checked by hand).
Profile share: not measured yet.

## Log
- 2026-09-25 filed from the codebase sweep.
