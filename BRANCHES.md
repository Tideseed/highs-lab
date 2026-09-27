# Branches on Tideseed/HiGHS (frozen 2026-09-27)

All branches are cut from upstream `latest` 6293630a84. The diff links compare against upstream latest; for exact
diffs, use `git diff 6293630a84...<branch>`. Size = files, +lines, −lines. Evidence: `vault/30-results/Final report.md`.

| branch | SHA | size | status | what |
|---|---|---|---|---|
| [lab/clique-partition-marking](https://github.com/Tideseed/HiGHS/compare/latest...lab/clique-partition-marking) | 39367bfe61 | 2, +59, −5 | in v4 | clique neighbour queries by marking; includes the find_common fix; s100 time-limit root cause |
| [lab/hash-tree-find-common](https://github.com/Tideseed/HiGHS/compare/latest...lab/hash-tree-find-common) | 6ecd07ee72 | 1, +7, −5 | reference | HighsHashTree::find_common false-negative fix alone (correctness) |
| [lab/symmetry-dense-hash](https://github.com/Tideseed/HiGHS/compare/latest...lab/symmetry-dense-hash) | 51ebf64d2f | 2, +30, −1 | in v4 | dense vertex hashes in symmetry refinement (identical search) |
| [lab/free-wins](https://github.com/Tideseed/HiGHS/compare/latest...lab/free-wins) | e1983642bf | 3, +12, −3 | in v4 | skip unused glpsol errors per LP; cache column maxima in presolve (identical search) |
| [lab/presolve-changed-col](https://github.com/Tideseed/HiGHS/compare/latest...lab/presolve-changed-col) | 5816d69698 | 2, +20, −2 | in v4 | P1: skip the markChangedCol column walk when no row is flagged (identical search) |
| [lab/dse-cache](https://github.com/Tideseed/HiGHS/compare/latest...lab/dse-cache) | 99b1bf1f8a | 3, +73, −1 | in v4 | restore DSE weights of a recent basis from a hash-keyed cache (search changes) |
| [lab/dual-substitution-mirrored](https://github.com/Tideseed/HiGHS/compare/latest...lab/dual-substitution-mirrored) | c81725e48f | 1, +57, −41 | experimental (X1) | mirrored dual substitution (x = y under big-M rows); neos-787933 win, losses elsewhere |
| lab/dse-carry-weights | 8dc4f6a81e | 3, +209, −3 | superseded | DSE cache + cut-row carry (the carry half was dropped) |
| lab/dse-split-diag | 76962346b1 | 3, +216, −3 | diagnostic | compile-flag switch cache-only / carry-only |
| lab/one-opt | bdf9d289c7 | 2, +70 | rejected | one-opt heuristic (never fired) |
| lab/locks-heuristic | 13995338e9 | 3, +106 | rejected | locks root heuristic (no effect) |

Combined arms: `dev-tideseed` = **base** (tag dev-tideseed-base, 23395de1c6: clique marking + find_common fix, symmetry dense hash, free wins, P1) since 2026-09-27 19:0x, per D-006's registered verdict (DSE dropped); v4 (tag dev-tideseed-v4, branch arm/dev-tideseed-v4, cfa835da83) = base + DSE cache; v3 (tag dev-tideseed-v3, 4a7937f32e) = v4 + X1; tags dev-tideseed-v1/v2 are historical. See `bench/COMPOSITION.md`.
