---
id: X6
area: mip
status: candidate
gate: full
effort: 3-5 d
verified_in_source: false
profiled_share: null
branch: null
---
# X6: Diving variants and adaptive LNS

**Where:** highs/mip/HighsSearch.cpp dive() (single plain dive); HighsPrimalHeuristics (RINS/RENS only)

**What:** SCIP found best solutions with adaptivediving, pscostdiving, farkasdiving, conflictdiving, alns, crossover on istanbul, CMS750_4, piperout-27, rail507.

**Proposed fix:** Guided/pscost diving and a crossover LNS first; adaptive selection later.

**Source:** static read of `latest` on 2026-09-25 (sweep agent, not yet checked by hand).
Measured share, branch and status: see frontmatter (kept current there only).

## Log
- 2026-09-25 filed from the codebase sweep.
