---
id: C2
area: presolve
status: candidate
gate: full
effort: 1-2 d
verified_in_source: true
profiled_share: 52% chromaticindex presolve
branch: null
---
# C2: Clique merging collectCliques

**Where:** highs/mip/HighsCliqueTable.cpp:131 cliqueSubsumption, :177 collectCliques (HashTree for_each per variable); called from HPresolve::finaliseProbing -> runCliqueMerging

**What:** chromaticindex1024-7: presolve 58 s of which cliqueSubsumption 52 % (collectCliques hash-tree traversal 34 % self).

**Proposed fix:** Flat per-variable clique lists or a cheaper subsumption test; developers active in cliques (#3312).

**Evidence so far:** static read of `latest` on 2026-09-25 (checked by hand).
Profile share: not measured yet.

## Log
- 2026-09-25 filed from the codebase sweep.
