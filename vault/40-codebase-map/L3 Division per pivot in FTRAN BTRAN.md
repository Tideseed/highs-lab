---
id: L3
area: factor
status: candidate
gate: full
effort: 0.5 d
verified_in_source: false
profiled_share: null
branch: null
---
# L3: Division per pivot in FTRAN BTRAN

**Where:** highs/util/HFactor.cpp:1813, 1911, 146, 48, 2047

**What:** pivot_multiplier /= u_pivot_value per pivot in every solve.

**Proposed fix:** Store reciprocal pivots (last-bit changes).

**Evidence so far:** static read of `latest` on 2026-09-25 (sweep agent, not yet checked by hand).
Profile share: not measured yet.

## Log
- 2026-09-25 filed from the codebase sweep.
