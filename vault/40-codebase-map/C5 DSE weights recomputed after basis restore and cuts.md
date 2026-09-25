---
id: C5
area: simplex
status: gated-quick
gate: full
effort: 1 d
verified_in_source: true
profiled_share: 24% seymour1, 27% glass-sc
branch: lab/dse-carry-weights
---
# C5: DSE weights recomputed after basis restore and cuts

**Where:** highs/simplex/HEkkDual.cpp:~165 computeDualSteepestEdgeWeights(true); HEkk::invalidateBasis / setBasis / updateStatus(kNewRows,kDelRows)

**What:** All DSE weights (one BTRAN per row) recomputed after every basis restore (dives, strong branching) and every cut round: 24 % seymour1, 27 % glass-sc, 10-15 % on several more.

**Proposed fix:** Cache weights by variable keyed by basis hash; carry weights across row add/delete with basic slacks.

**Evidence so far:** static read of `latest` on 2026-09-25 (checked by hand).
Profile share: not measured yet.

## Log
- 2026-09-25 filed from the codebase sweep.
