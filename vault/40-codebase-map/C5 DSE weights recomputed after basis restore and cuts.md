---
id: C5
area: simplex
status: merged (decision pending D-004 rule 2)
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

**Source:** static read of `latest` on 2026-09-25 (checked by hand).
Measured share, branch and status: see frontmatter (kept current there only).

## Log
- 2026-09-25 filed from the codebase sweep.
- 2026-09-25 evening, upstream cross-check (review #3/#4): ERGO-Code PR #685 (merged 2022-01, "DSE weight
  preservation") already keeps the weights across bound/cost changes and simplex rebuilds ("still some scope for
  more"). Issue #2230 (closed) covers warm starts and scaling. PR #688 (unmerged) was superseded and reported sudden
  weight errors in strong branching → regression target. What lab/dse-carry-weights ADDS on top of #685, by path:
  (a) `HEkk::invalidateBasis` / `HEkk::setBasis(HighsBasis)`: a basis restore (dive backtrack, strong-branching
      candidate reset via HighsLpRelaxation::recoverBasis/setStoredBasis) cleared the weights → now restored from a
      hash-keyed cache (filled at the end of each solve and before a basis is replaced);
  (b) `HEkk::addRows` / `deleteRows` (cut rounds) → `updateStatus(kNewRows/kDelRows)` → `HEkk::clear()` → now carried
      by variable, only new rows recomputed.
  Measured before the change (perf, 60 s): recomputation 24 % seymour1, 27 % glass-sc, 10–15 % comp21-2idx, tr12-30,
  roll3000, binkar10_1, timtab1; on seymour1 ~2/3 of it from (a) (dives 13 %, strong branching 7 %).
  Decision rule for keeping it: [[D-004 Decision rules for tonight]] rule 2.
