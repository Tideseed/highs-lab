---
id: B1
area: build
status: candidate
gate: full
effort: hours
verified_in_source: false
profiled_share: null
branch: null
---
# B1: Build flags mcpu LTO PGO

**Where:** CMakeLists.txt:446-467 (LTO off for static, forced off with CUDA), :540-555 (-mpopcnt only), no -march/-mcpu, no PGO

**What:** Wheels and default builds are generic armv8-a -O3 without LTO.

**Proposed fix:** -mcpu=native, IPO on, then PGO with a training set disjoint from the screening set.

**Evidence so far:** static read of `latest` on 2026-09-25 (sweep agent, not yet checked by hand).
Profile share: not measured yet.

## Log
- 2026-09-25 filed from the codebase sweep.
