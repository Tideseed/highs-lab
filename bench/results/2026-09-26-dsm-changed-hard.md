# Hard-set comparison `results/raw/2026-09-26-dsm-changed` (control `dev`)

108 runs; 0 without a logged trajectory (PDGI from final bounds).

| arm | pairs (inst) | PDGI arm / ctl | ΔPDGI [95% CI, instance bootstrap] | solved (ctl) | feasible (ctl) | mean final gap % (ctl) | overrun mean/max s (ctl max) | wrong | crashed | ref coverage |
|---|---|---|---|---|---|---|---|---|---|---|
| lab-dsm | 54 (27) | 0.4854 / 0.4797 | +0.0056 [-0.0197, +0.0273] | 21 (22) | 38 (39) | 42.1 (38.9) | 3.7/33.0 (36.2) | 0 | 0 | 52/54 |

PDGI: normalised primal-dual gap integral over the fixed horizon (0 best, 1 = no usable bounds throughout). ΔPDGI < 0 favours the arm; the CI resamples instances with their seeds kept together.

## Instances with |ΔPDGI| ≥ 0.05 (seed mean), wrong answers, crashes

| arm | instance | ΔPDGI / note |
|---|---|---|
| lab-dsm | neos-787933 | -0.257 |
| lab-dsm | bab6 | +0.070 |
| lab-dsm | neos-4722843-widden | +0.110 |
| lab-dsm | comp07-2idx | +0.142 |
