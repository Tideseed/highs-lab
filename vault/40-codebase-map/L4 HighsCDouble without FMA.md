---
id: L4
area: util
status: candidate
gate: identical expected
effort: 2-4 h
verified_in_source: false
profiled_share: null
branch: null
---
# L4: HighsCDouble without FMA

**Where:** highs/util/HighsCDouble.h:51; HighsLinearSumBounds.cpp:197

**What:** Dekker two_product where FMA exists; +-1 multiplied as double-double. Also check the -ffp-contract exactness risk.

**Proposed fix:** std::fma two-product; fold the sign first.

**Source:** static read of `latest` on 2026-09-25 (sweep agent, not yet checked by hand).
Measured share, branch and status: see frontmatter (kept current there only).

## Log
- 2026-09-25 filed from the codebase sweep.
