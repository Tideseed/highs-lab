---
id: X4
area: mip
status: candidate
gate: full
effort: 2-3 d
verified_in_source: false
profiled_share: null
branch: null
---
# X4: Lifted flow cover separator

**Where:** highs/mip/HighsSeparation.cpp (missing dedicated flow cover; HiGHS has path aggregation + c-MIR)

**What:** SCIP applied flow-cover cuts on 7/12 SCIP-win instances (CMS750_4 3508, krka 2997, cbs-cta 417, istanbul 1963).

**Proposed fix:** Flow cover on single-node flow relaxations of aggregated rows (Gu-Nemhauser-Savelsbergh lifting).

**Source:** static read of `latest` on 2026-09-25 (sweep agent, not yet checked by hand).
Measured share, branch and status: see frontmatter (kept current there only).

## Log
- 2026-09-25 filed from the codebase sweep.
