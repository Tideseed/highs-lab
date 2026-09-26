# Hard-set comparison `results/raw/2026-09-26-dse-split` (control `dev`)

108 runs; 0 without a logged trajectory (PDGI from final bounds).

| arm | pairs (inst) | PDGI arm / ctl | ΔPDGI [95% CI, instance bootstrap] | solved (ctl) | feasible (ctl) | mean final gap % (ctl) | overrun mean/max s (ctl max) | wrong | crashed | ref coverage |
|---|---|---|---|---|---|---|---|---|---|---|
| dse-cache | 27 (9) | 0.1304 / 0.1307 | -0.0003 [-0.0011, +0.0005] | 18 (18) | 27 (27) | 11.3 (11.2) | 0.1/0.2 (0.2) | 0 | 0 | 27/27 |
| dse-carry | 27 (9) | 0.1338 / 0.1307 | +0.0031 [-0.0007, +0.0098] | 18 (18) | 27 (27) | 11.3 (11.2) | 0.1/0.4 (0.2) | 0 | 0 | 27/27 |
| lab-dse | 27 (9) | 0.1333 / 0.1307 | +0.0025 [-0.0013, +0.0091] | 18 (18) | 27 (27) | 11.5 (11.2) | 0.1/0.2 (0.2) | 0 | 0 | 27/27 |

PDGI: normalised primal-dual gap integral over the fixed horizon (0 best, 1 = no usable bounds throughout). ΔPDGI < 0 favours the arm; the CI resamples instances with their seeds kept together.

