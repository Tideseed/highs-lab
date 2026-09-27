# Hard-set comparison `results/raw/2026-09-27-clean2-ablation` (control `dts-v2-nodse`)

90 runs; 0 without a logged trajectory (PDGI from final bounds); 10 whose last progress row is >60 s before the end (final bounds appended at the end).

| arm | pairs (inst) | PDGI arm / ctl | ΔPDGI [95% CI, instance bootstrap] | solved (ctl) | feasible (ctl) | mean final gap % (ctl) | overrun mean/max s (ctl max) | wrong | crashed | known-optimum coverage |
|---|---|---|---|---|---|---|---|---|---|---|
| base-x1 | 18 (9) | 0.2556 / 0.2580 | -0.0024 [-0.0754, +0.0583] | 14 (12) | 16 (16) | 13.6 (14.9) | 531.4/1065.4 (1019.4) | 0 | 0 | 16/18 |
| dev | 18 (9) | 0.2705 / 0.2580 | +0.0125 [+0.0003, +0.0292] | 12 (12) | 16 (16) | 14.9 (14.9) | 188.1/1005.9 (1019.4) | 0 | 0 | 16/18 |
| dts-v3 | 18 (9) | 0.2448 / 0.2580 | -0.0132 [-0.0780, +0.0357] | 13 (12) | 16 (16) | 13.6 (14.9) | 420.6/1063.4 (1019.4) | 0 | 0 | 16/18 |
| dts-v4 | 18 (9) | 0.2653 / 0.2580 | +0.0073 [-0.0004, +0.0185] | 12 (12) | 16 (16) | 15.6 (14.9) | 175.0/1012.3 (1019.4) | 0 | 0 | 16/18 |

PDGI: normalised primal-dual gap integral over the fixed horizon (0 best, 1 = no usable bounds throughout). ΔPDGI < 0 favours the arm; the CI resamples instances with their seeds kept together.

## Instances with |ΔPDGI| ≥ 0.05 (seed mean), wrong answers, crashes

| arm | instance | ΔPDGI / note |
|---|---|---|
| base-x1 | neos-787933 | -0.239 |
| base-x1 | neos-4722843-widden | +0.119 |
| base-x1 | comp07-2idx | +0.137 |
| dev | neos-4722843-widden | +0.074 |
| dts-v3 | neos-787933 | -0.237 |
| dts-v3 | neos-4722843-widden | +0.055 |
| dts-v3 | comp07-2idx | +0.101 |
