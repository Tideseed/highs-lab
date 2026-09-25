# Hard-set comparison `results/raw/2026-09-25-3arm-hard` (control `dev`)

378 runs; 0 without a logged trajectory (PDGI from final bounds).

| arm | pairs (inst) | PDGI arm / ctl | ΔPDGI [95% CI, instance bootstrap] | solved (ctl) | feasible (ctl) | mean final gap % (ctl) | overrun mean/max s (ctl max) | wrong | crashed | ref coverage |
|---|---|---|---|---|---|---|---|---|---|---|
| dev-tideseed | 126 (42) | 0.6003 / 0.6046 | -0.0043 [-0.0159, +0.0034] | 2 (1) | 100 (97) | 55.3 (55.5) | 1.0/25.1 (282.4) | 0 | 0 | 126/126 |
| stable | 126 (42) | 0.6539 / 0.6046 | +0.0493 [+0.0080, +0.1030] | 0 (1) | 96 (97) | 61.8 (55.5) | 6.9/285.8 (282.4) | 0 | 0 | 126/126 |

PDGI: normalised primal-dual gap integral over the fixed horizon (0 best, 1 = no usable bounds throughout). ΔPDGI < 0 favours the arm; the CI resamples instances with their seeds kept together.

## Instances with |ΔPDGI| ≥ 0.05 (seed mean), wrong answers, crashes

| arm | instance | ΔPDGI / note |
|---|---|---|
| dev-tideseed | neos-3004026-krka | -0.197 |
| dev-tideseed | supportcase42 | +0.060 |
| stable | dws008-01 | -0.063 |
| stable | neos-787933 | -0.062 |
| stable | glass-sc | +0.052 |
| stable | neos-1171737 | +0.055 |
| stable | supportcase42 | +0.060 |
| stable | sing326 | +0.065 |
| stable | rail507 | +0.074 |
| stable | comp21-2idx | +0.093 |
| stable | CMS750_4 | +0.453 |
| stable | sorrell3 | +0.550 |
| stable | neos-3046615-murg | +0.753 |
