# MIPFEAS-style primal integral `results/raw/2026-09-27-clean2-ablation` (control `dev`)

80 runs on instances with a finite reference value; T = 300.0 s. Score per run: Mittelmann's primal integral P in [0, 2] (lower is better); table: shifted geometric mean (shift 0.001) over instances (seeds averaged first), ratio vs control with a paired instance bootstrap.

| arm | inst | SGM P | ratio vs ctl [95% CI] | mean P | feasible runs | SGM t first incumbent (s, found only) | within 1 % of z* by T | within 1e-4 by T |
|---|---|---|---|---|---|---|---|---|
| base-x1 | 8 | 0.0483 | 0.976 [0.647, 1.366] | 0.0992 | 16/16 | 3.3 | 14/16 | 14/16 |
| dev | 8 | 0.0495 | 1.000 [1.000, 1.000] | 0.0905 | 16/16 | 3.7 | 14/16 | 14/16 |
| dts-v2-nodse | 8 | 0.0480 | 0.968 [0.909, 1.012] | 0.0843 | 16/16 | 3.5 | 14/16 | 14/16 |
| dts-v3 | 8 | 0.0474 | 0.958 [0.677, 1.267] | 0.0939 | 16/16 | 3.3 | 14/16 | 13/16 |
| dts-v4 | 8 | 0.0480 | 0.968 [0.918, 1.021] | 0.0868 | 16/16 | 3.6 | 13/16 | 13/16 |

## Runs with no incumbent by T

- **base-x1** (0): 
- **dev** (0): 
- **dts-v2-nodse** (0): 
- **dts-v3** (0): 
- **dts-v4** (0): 

## Largest per-instance differences (|ΔP| ≥ 0.05, seed mean)

| arm | instance | P arm | P ctl | ΔP |
|---|---|---|---|---|
| base-x1 | neos-787933 | 0.026 | 0.089 | -0.063 |
| base-x1 | comp07-2idx | 0.248 | 0.114 | +0.134 |
| dts-v3 | neos-787933 | 0.031 | 0.089 | -0.059 |
| dts-v3 | comp07-2idx | 0.213 | 0.114 | +0.099 |
