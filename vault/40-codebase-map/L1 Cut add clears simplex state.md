---
id: L1
area: simplex
status: candidate
gate: full
effort: 2-4 d
verified_in_source: true
profiled_share: null
branch: null
---
# L1: Cut add clears simplex state

**Where:** highs/lp_data/HConst.h:46 kExtendInvertWhenAddingRows=false; highs/simplex/HEkk.cpp:313-357 updateStatus; HEkk.cpp:2084 DSE recompute; highs/util/HFactorExtend.cpp dormant

**What:** Every cut add/delete calls HEkk::clear(): factor, DSE weights, row-wise matrix discarded; the next solve recomputes DSE weights (m BTRANs) or falls back to Devex. Largest suspected MIP cost.

**Proposed fix:** Enable row extension; keep old DSE weights and compute new cut weights (one BTRAN each); compact on delete.

**Source:** static read of `latest` on 2026-09-25 (checked by hand).
Measured share, branch and status: see frontmatter (kept current there only).

## Log
- 2026-09-25 filed from the codebase sweep.
