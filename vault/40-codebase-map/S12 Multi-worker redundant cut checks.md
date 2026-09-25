---
id: S12
area: mip
status: candidate
gate: full (parallel)
effort: 1 d
verified_in_source: false
profiled_share: null
branch: null
---
# S12: Multi-worker redundant cut checks

**Where:** highs/mip/HighsSeparation.cpp:151; HighsCutPool.cpp:248

**What:** Workers re-check violation of global cuts already in their LP; each bound change walks two dynamic cut matrices.

**Proposed fix:** Per-worker in-LP bitmap; static global pool between syncs.

**Source:** static read of `latest` on 2026-09-25 (sweep agent, not yet checked by hand).
Measured share, branch and status: see frontmatter (kept current there only).

## Log
- 2026-09-25 filed from the codebase sweep.
