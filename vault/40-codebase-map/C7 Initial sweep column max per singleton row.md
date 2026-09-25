---
id: C7
area: presolve
status: branch
gate: identical
effort: 15 min
verified_in_source: true
profiled_share: 13% toguru
branch: lab/free-wins
---
# C7: Initial sweep column max per singleton row

**Where:** highs/presolve/HPresolveInitialSweep.cpp:121,147 getMaxAbsColVal

**What:** Column max recomputed per singleton row; LP presolve runs inside root heuristics on toguru: 13 %.

**Proposed fix:** Cache per column.

**Evidence so far:** static read of `latest` on 2026-09-25 (checked by hand).
Profile share: not measured yet.

## Log
- 2026-09-25 filed from the codebase sweep.
