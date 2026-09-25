# Arm composition (keep in sync with bench/queue.txt and bench/arms.toml)

Source SHAs are also recorded per run in each `RESOURCES-*.json` (`arms.<name>.build.source_sha`, compiler,
effective flags, `source_dirty`) and per result (`binary_sha` = executable + libhighs, `model_sha`).

| arm (arms.toml) | fork ref | source SHA | composition |
|---|---|---|---|
| stable | tag v1.15.1 (upstream) | 04024d701f | latest release |
| dev | upstream/latest | 6293630a84 | control |
| dev-tideseed (v1, historical) | tag dev-tideseed-v1 | see tag | clique marking (count bug: query count differed from pairwise) + symmetry + free-wins + DSE |
| dts-v2 | branch dev-tideseed, tag dev-tideseed-v2 | 9e9a3f98f2 | latest + clique-partition-marking 39367bfe61 + symmetry-dense-hash 51ebf64d2f + free-wins e1983642bf + dse-carry-weights 8dc4f6a81e + presolve-changed-col 5816d69698 |
| dts-v2-nodse | branch dev-tideseed-nodse | 23395de1c6 | dts-v2 without dse-carry-weights |
| dts-native / dts-pgo | v1 source | — | build-flag arms (see vault note Build flags) |

Build: GCC 13.3, Release (-O3 -DNDEBUG), shared library with LTO (-flto=auto, HiGHS default), no -mcpu unless named.
