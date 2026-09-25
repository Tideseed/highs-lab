---
id: T2
area: presolve
status: candidate
gate: full
effort: 2-4 h
verified_in_source: true
profiled_share: null
branch: null
---
# T2: Presolve clique merging ignores time limit

**Where:** highs/presolve/HPresolve.cpp:1947 finaliseProbing -> HighsCliqueTable::runCliqueMerging (no timer)

**What:** chromaticindex1024-7 with time_limit=60: presolve 58 s, total 85-110 s.

**Proposed fix:** Pass a deadline into runCliqueMerging / check between cliques.

**Evidence so far:** static read of `latest` on 2026-09-25 (checked by hand).
Profile share: not measured yet.

## Log
- 2026-09-25 filed from the codebase sweep.
