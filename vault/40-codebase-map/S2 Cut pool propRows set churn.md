---
id: S2
area: mip
status: candidate
gate: identical
effort: 2 h / 0.5 d
verified_in_source: true
profiled_share: null
branch: null
---
# S2: Cut pool propRows set churn

**Where:** highs/mip/HighsCutPool.h:106-116 resetAge; HighsCutPool.cpp:273,306,340

**What:** std::set erase+emplace (node free+malloc) on every age reset of a propagated cut, every round.

**Proposed fix:** extract() node handle (quick) or per-age buckets.

**Evidence so far:** static read of `latest` on 2026-09-25 (checked by hand).
Profile share: not measured yet.

## Log
- 2026-09-25 filed from the codebase sweep.
