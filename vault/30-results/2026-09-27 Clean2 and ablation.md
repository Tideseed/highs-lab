# Clean2 (2026-09-27 00:15–03:51): dev vs dts-v4 seed 1 + ablation — last experiments before the freeze

Clean window (both LLM servers stopped, box-window lease, 10 X925 lanes, 8 GB/run, 300 s). Freeze from 07:15.

## dev vs dts-v4 (= v3 without X1: clique marking + symmetry + free wins + P1 + dse-cache), seed 1, 240 instances
| | SGM ratio [95 % CI] | both-solved | solved | ΔPDGI [CI] | wrong | crashed |
|---|---|---|---|---|---|---|
| dts-v4 vs dev | **0.969 [0.939, 0.996]** | 0.933 | **101 vs 98** | **−0.0104 [−0.0192, −0.0023]** | 0 | 0 |
Passes the gate on this seed (ratio ≤ 0.97, CI < 1, 0 wrong, 0 crashed, solved ≥ dev). NOT replicated: v4 was not
run on seed 0; v3 (= v4 + X1) on seed 0 was 0.985 [0.942, 1.022]. `bench/results/2026-09-27-clean2*.md`.

## Ablation (control = base = the four identical-search branches), 9 instances × 2 seeds, 300 s
| instance | dev | base | +cache | +X1 | +both (v3) |
|---|---|---|---|---|---|
| neos-787933 | lim, lim | lim, lim | lim, lim | **5 s, 3 s** | **5 s, 4 s** |
| neos-873061 | 99, 237 | 97, 228 | 116, 231 | 297, 171 | lim, 218 |
| comp07-2idx | 46, 42 | 47, 41 | 47, 39 | 33, **294** | 32, **239** |
| neos-4722843-widden | 164, 166 | 113, 147 | 168, 147 | 181, 251 | 196, 251 |
| csched008 | 176, 153 | 177, 152 | 216, 149 | 176, 153 | 214, 149 |
| neos-5114902-kasavu | 300, **1300 (+1005)** | 301, 1314 (+1019) | 301, 1306 (+1012) | 1360 (+1065), 1323 | 1358, 1302 |
| neos-3402454-bohle | lim +62, lim +52 | lim, lim | lim, lim | lim, lim | lim, lim |
| n5-3, unitcal_7 | ~equal | | | X1 slower on unitcal_7 s1 (68 vs 43) | |

Conclusions: (1) **kasavu's overrun is seed-dependent and present in dev (latest) itself** — not our regression;
yesterday's "regression vs latest" correction was wrong (it rested on one seed). (2) **X1** is the cause of the
neos-873061 / comp07 s1 / widden losses and of the neos-787933 win. (3) **dse-cache** is neutral on these except
csched008 s0 (216 vs 177 s). (4) bohle: dev overruns the limit by 52–62 s here; our arms stop on time; no memory kill
this time (8 GB cap).
