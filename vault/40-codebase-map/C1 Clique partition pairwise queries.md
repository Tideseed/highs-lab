---
id: C1
area: mip
status: gated-quick
gate: identical
effort: done (branch)
verified_in_source: true
profiled_share: 90% (s100)
branch: lab/clique-partition-marking
---
# C1: Clique partition pairwise queries

**Where:** highs/mip/HighsCliqueTable.cpp cliquePartition (both overloads) -> partitionNeighbourhood -> queryNeighbourhood -> findCommonCliqueId; called from HighsObjectiveFunction::setupCliquePartition in HighsMipSolverData::runSetup

**What:** Greedy clique partition of the objective binaries runs one hash-tree intersection per (vertex, remaining candidate) pair. On s100 (cliques of ~5000) that is ~1.1e9 queries at ~90 ns = ~140 s before the first node, with no time check. Found by perf, 2026-09-25: 90 % of s100's run.

**Proposed fix:** Mark the entries of v's cliques, scan the window once; pairwise only if marking touches >16x the window. Identical result and query count.

**Evidence so far:** static read of `latest` on 2026-09-25 (checked by hand).
Profile share: not measured yet.

## Log
- 2026-09-25 filed from the codebase sweep.
- 2026-09-25 lab/clique-partition-marking 6ad70a8ec3: s100 time_limit=60: 172 s wall, 0 nodes, no solution → 62 s wall, feasible, gap 57 %. Quick screen (21 instances): identical search, time neutral.
