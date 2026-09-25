# Build flags: -mcpu=native and PGO (2026-09-25 15:05)

dev-tideseed v1 source, three builds: default (Release, -O3, LTO already on for the shared lib), `-mcpu=native`,
PGO (`-mcpu=native -fprofile-use`, trained 12 × 30 s on non-MIPLIB families: 6 PGLib-UC, 3 ML4CO item placement,
3 ML4CO load balancing — disjoint from every benchmark set). Small set, 33 instances, seeds 0–1, 120 s, X925 cores.
`bench/results/2026-09-25-buildflags.md`.

| build | SGM ratio vs default [95 % CI] | both-solved | identical search |
|---|---|---|---|
| -mcpu=native | 1.004 [0.992, 1.018] | 1.005 | 56/56 |
| PGO | **0.970 [0.949, 0.989]** | 0.961 | 56/56 |

- LTO: already on by default for the shared library (not for static builds, and forced off with CUDA).
- `-mcpu=native` (Cortex-X925, GCC 13): no effect.
- PGO: ~3 % faster, identical search → a pure build win. It is a build choice, so it would speed up upstream latest
  equally; kept out of the code comparison (dev vs dev-tideseed). Candidate recommendation for wheel builds.
- A slow-core spot check earlier (3 instances, A725, parallel load) showed ±1 % — too small a sample; this run supersedes it.
