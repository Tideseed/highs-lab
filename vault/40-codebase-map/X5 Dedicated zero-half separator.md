---
id: X5
area: mip
status: candidate
gate: full
effort: 0.5 d analysis
verified_in_source: false
profiled_share: null
branch: null
---
# X5: Dedicated zero-half separator

**Where:** highs/mip/HighsModkSeparator.cpp (mod-k covers k=2 partially)

**What:** SCIP zerohalf applied on 7/12 (krka 5836 cuts, seymour1 174, rail507 103 = the only cuts on rail507).

**Proposed fix:** Compare HiGHS mod-2 output with SCIP zerohalf on these instances before implementing anything.

**Source:** static read of `latest` on 2026-09-25 (sweep agent, not yet checked by hand).
Measured share, branch and status: see frontmatter (kept current there only).

## Log
- 2026-09-25 filed from the codebase sweep.
