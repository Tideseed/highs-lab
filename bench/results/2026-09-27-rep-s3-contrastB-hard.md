# Hard-set comparison `/home/coulson/git_repositories/highs-lab/bench/results/raw/2026-09-27-rep-s3` (control `dts-v2-nodse`)

720 runs; 0 without a logged trajectory (PDGI from final bounds); 183 whose last progress row is >60 s before the end (final bounds appended at the end).

| arm | pairs (inst) | PDGI arm / ctl | ΔPDGI [95% CI, instance bootstrap] | solved (ctl) | incumbent by T (ctl) | feasible at termination (ctl) | mean final gap % (ctl) | overrun mean/max s (ctl max) | wrong | crashed | known-optimum coverage |
|---|---|---|---|---|---|---|---|---|---|---|---|
| dev | 240 (240) | 0.3522 / 0.3501 | +0.0021 [-0.0007, +0.0046] | 93 (96) | 211 (210) | 211 (211) | 26.1 (26.2) | 8.0/902.5 (791.1) | 0 | 0 | 232/240 |
| dts-v4 | 240 (240) | 0.3449 / 0.3501 | -0.0052 [-0.0117, +0.0012] | 98 (96) | 210 (210) | 210 (211) | 25.6 (26.2) | 7.9/782.9 (791.1) | 0 | 1 | 232/240 |

PDGI: normalised primal-dual gap integral over the fixed horizon (0 best, 1 = no usable bounds throughout). ΔPDGI < 0 favours the arm; the CI resamples instances with their seeds kept together.

## Instances with |ΔPDGI| ≥ 0.05 (seed mean), wrong answers, crashes

| arm | instance | ΔPDGI / note |
|---|---|---|
| dev | neos-950242 | -0.210 |
| dev | buildingenergy | -0.087 |
| dev | neos-5114902-kasavu | +0.051 |
| dev | neos-4722843-widden | +0.053 |
| dev | savsched1 | +0.065 |
| dev | bab6 | +0.080 |
| dev | s250r10 | +0.082 |
| dev | k1mushroom | +0.118 |
| dts-v4 | momentum1 | -0.404 |
| dts-v4 | radiationm18-12-05 | -0.266 |
| dts-v4 | neos-950242 | -0.210 |
| dts-v4 | 30n20b8 | -0.206 |
| dts-v4 | pk1 | -0.165 |
| dts-v4 | csched007 | -0.131 |
| dts-v4 | rocI-4-11 | -0.125 |
| dts-v4 | supportcase42 | -0.099 |
| dts-v4 | bab2 | -0.082 |
| dts-v4 | neos-2746589-doon | -0.080 |
| dts-v4 | lectsched-5-obj | -0.079 |
| dts-v4 | neos-3004026-krka | -0.061 |
| dts-v4 | glass4 | -0.051 |
| dts-v4 | neos-1456979 | -0.050 |
| dts-v4 | fastxgemm-n2r6s0t2 | +0.058 |
| dts-v4 | neos-787933 | +0.061 |
| dts-v4 | ns1830653 | +0.105 |
| dts-v4 | neos-3024952-loue | +0.293 |
| dts-v4 | traininstance6 | +0.295 |
| dts-v4 | neos-3402454-bohle s3 | CRASH rc=-15 |
