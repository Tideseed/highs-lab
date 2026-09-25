---
id: L2
area: simplex
status: candidate
gate: identical if exact
effort: 2-3 d
verified_in_source: false
profiled_share: null
branch: null
---
# L2: Rescale and rebuild row-wise matrix per LP

**Where:** highs/simplex/HApp.h:171,284; HEkk.cpp:414

**What:** Each LP run scales, rebuilds the AR matrix and unscales: ~3 x O(nnz) even for tiny dive/strong-branching LPs.

**Proposed fix:** Keep scaled LP and AR matrix across bound/cost-only changes.

**Evidence so far:** static read of `latest` on 2026-09-25 (sweep agent, not yet checked by hand).
Profile share: not measured yet.

## Log
- 2026-09-25 filed from the codebase sweep.
