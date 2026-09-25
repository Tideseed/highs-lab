---
id: B1
area: build
status: measured
gate: full
effort: hours
verified_in_source: false
profiled_share: n/a (PGO -3.0 % time, native 0 %)
branch: null
---
# B1: Build flags mcpu LTO PGO

**Where:** CMakeLists.txt:446-467 (LTO off for static, forced off with CUDA), :540-555 (-mpopcnt only), no -march/-mcpu, no PGO

**What:** Wheels and default builds are generic armv8-a -O3 without LTO.

**Proposed fix:** -mcpu=native, IPO on, then PGO with a training set disjoint from the screening set.

**Source:** static read of `latest` on 2026-09-25 (sweep agent, not yet checked by hand).
Measured share, branch and status: see frontmatter (kept current there only).

## Log
- 2026-09-25 filed from the codebase sweep.
- 2026-09-25 measured: PGO 0.970 [0.949,0.989] identical search; -mcpu=native 1.004; LTO already default for shared builds. See [[2026-09-25 Build flags native and PGO]].
