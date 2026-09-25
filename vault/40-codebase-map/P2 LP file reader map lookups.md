---
id: P2
area: io
status: candidate
gate: identical model
effort: 0.5 d
verified_in_source: false
profiled_share: null
branch: null
---
# P2: LP file reader map lookups

**Where:** highs/io/FilereaderLp.cpp:121-200; reader.cpp:382

**What:** std::map keyed by shared_ptr: ~7 tree lookups and 2 allocations per nonzero.

**Proposed fix:** Integer ids, two-pass CSC fill.

**Evidence so far:** static read of `latest` on 2026-09-25 (sweep agent, not yet checked by hand).
Profile share: not measured yet.

## Log
- 2026-09-25 filed from the codebase sweep.
