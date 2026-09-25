---
id: S6
area: mip
status: candidate
gate: identical
effort: 0.5 d
verified_in_source: false
profiled_share: null
branch: null
---
# S6: pruneInfeasibleNodes full scans

**Where:** highs/mip/HighsNodeQueue.cpp:274-297

**What:** Two O(numCol) scans and a std::set per node batch.

**Proposed fix:** Changed columns only; vector+sort/unique.

**Evidence so far:** static read of `latest` on 2026-09-25 (sweep agent, not yet checked by hand).
Profile share: not measured yet.

## Log
- 2026-09-25 filed from the codebase sweep.
