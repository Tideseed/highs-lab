# DRAFT — comment on ERGO-Code/HiGHS#3314 (not posted; needs Berk's yes)

Prior art: none beyond #3314 itself (0 comments as of 2026-09-25 13:10).

---

> Note: I am Claude Code (Anthropic's coding agent), adding this on behalf of Berk Orbay (@berkorbay), who filed the
> issue with me. Per CONTRIBUTING.md this is a report, not a pull request.

We traced the overrun on s100. It reproduces on `latest` (6293630a84): time_limit=60, threads=1 → 172 s, 0 nodes.

`perf` shows 90 % of the run in `HighsObjectiveFunction::setupCliquePartition` (called from
`HighsMipSolverData::runSetup`) → `HighsCliqueTable::cliquePartition` → `partitionNeighbourhood` →
`queryNeighbourhood` → `findCommonCliqueId`. s100 has cliques of ~5000 binaries; the greedy partition queries every
remaining candidate pairwise (one `HighsHashTree::find_common` per pair), ~1.1e9 queries at ~90 ns each. There is no
time-limit check in that phase, which is why the limit is exceeded before the first node.

What we tried (branch for illustration: https://github.com/Tideseed/HiGHS/compare/latest...lab/clique-partition-marking):
in `queryNeighbourhood`, mark the entries of the cliques containing `v` once and scan the candidates, falling back to
pairwise queries when marking would touch >16x as many entries as there are candidates; skip entries of deleted
columns and the column of `v`, as `haveCommonClique` does; keep `numNeighbourhoodQueries` advancing as before. With
that, s100 stops at 62 s with a feasible solution (gap 57 %). We checked the marking result against the pairwise
queries on every call on 10 MIPLIB instances — this is how we found #NNNN (find_common false negatives), which has to
be fixed for the two to agree.

A time check after `setupCliquePartition` (or inside it) would still be worth having for the general case.
