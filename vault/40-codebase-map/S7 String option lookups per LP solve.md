---
id: S7
area: mip
status: candidate
gate: identical
effort: 2-4 h
verified_in_source: false
profiled_share: null
branch: null
---
# S7: String option lookups per LP solve

**Where:** highs/mip/HighsLpRelaxation.cpp:1131-1218

**What:** >=5 getOptionIndex linear string scans (~200 records) per LP solve.

**Proposed fix:** Cache OptionRecord pointers or write the options struct directly.

**Evidence so far:** static read of `latest` on 2026-09-25 (sweep agent, not yet checked by hand).
Profile share: not measured yet.

## Log
- 2026-09-25 filed from the codebase sweep.
