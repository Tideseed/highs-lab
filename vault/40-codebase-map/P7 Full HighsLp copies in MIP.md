---
id: P7
area: mip
status: candidate
gate: identical
effort: 0.5 d
verified_in_source: false
profiled_share: null
branch: null
---
# P7: Full HighsLp copies in MIP

**Where:** HPresolve.cpp:121; HighsLpRelaxation.cpp:222,239; HighsMipSolverData.cpp:1202,1353

**What:** 5-8 full model copies incl. names per MIP run.

**Proposed fix:** Field-by-field, no names.

**Evidence so far:** static read of `latest` on 2026-09-25 (sweep agent, not yet checked by hand).
Profile share: not measured yet.

## Log
- 2026-09-25 filed from the codebase sweep.
