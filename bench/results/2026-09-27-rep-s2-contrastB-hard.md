# Hard-set comparison `/home/coulson/git_repositories/highs-lab/bench/results/raw/2026-09-27-rep-s2` (control `dts-v2-nodse`)

720 runs; 0 without a logged trajectory (PDGI from final bounds); 188 whose last progress row is >60 s before the end (final bounds appended at the end).

| arm | pairs (inst) | PDGI arm / ctl | ΔPDGI [95% CI, instance bootstrap] | solved (ctl) | incumbent by T (ctl) | feasible at termination (ctl) | mean final gap % (ctl) | overrun mean/max s (ctl max) | wrong | crashed | known-optimum coverage |
|---|---|---|---|---|---|---|---|---|---|---|---|
| dev | 240 (240) | 0.3513 / 0.3519 | -0.0005 [-0.0064, +0.0036] | 96 (99) | 208 (208) | 208 (208) | 25.9 (25.7) | 2.1/208.2 (252.1) | 0 | 0 | 232/240 |
| dts-v4 | 240 (240) | 0.3468 / 0.3519 | -0.0051 [-0.0109, -0.0004] | 98 (99) | 207 (208) | 207 (208) | 25.7 (25.7) | 1.3/253.8 (252.1) | 0 | 1 | 232/240 |

PDGI: normalised primal-dual gap integral over the fixed horizon (0 best, 1 = no usable bounds throughout). ΔPDGI < 0 favours the arm; the CI resamples instances with their seeds kept together.

## Instances with |ΔPDGI| ≥ 0.05 (seed mean), wrong answers, crashes

| arm | instance | ΔPDGI / note |
|---|---|---|
| dev | physiciansched3-3 | -0.543 |
| dev | blp-ar98 | -0.134 |
| dev | bab2 | -0.054 |
| dev | triptim1 | +0.052 |
| dev | s250r10 | +0.073 |
| dev | neos-4722843-widden | +0.078 |
| dev | neos-950242 | +0.226 |
| dts-v4 | momentum1 | -0.445 |
| dts-v4 | comp07-2idx | -0.218 |
| dts-v4 | 30n20b8 | -0.181 |
| dts-v4 | traininstance6 | -0.170 |
| dts-v4 | ns1830653 | -0.147 |
| dts-v4 | satellites2-40 | -0.113 |
| dts-v4 | istanbul-no-cutoff | -0.088 |
| dts-v4 | radiationm18-12-05 | -0.075 |
| dts-v4 | buildingenergy | -0.073 |
| dts-v4 | neos-4722843-widden | -0.063 |
| dts-v4 | bab2 | -0.054 |
| dts-v4 | triptim1 | +0.052 |
| dts-v4 | eilA101-2 | +0.066 |
| dts-v4 | physiciansched3-3 | +0.077 |
| dts-v4 | neos-3004026-krka | +0.077 |
| dts-v4 | pk1 | +0.130 |
| dts-v4 | neos-3402454-bohle s2 | CRASH rc=-15 |
