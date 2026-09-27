# Bench analysis: `/home/coulson/git_repositories/highs-lab/bench/results/raw/2026-09-27-clean2-ablation`

control = `dts-v2-nodse`, 90 runs, arms: base-x1, dev, dts-v2-nodse, dts-v3, dts-v4

| arm | n inst | solved | SGM all (s) | ratio vs control [95% CI] | SGM both-solved | ratio | mean overrun (s) | max overrun (s) | wrong | crashed |
|---|---|---|---|---|---|---|---|---|---|---|
| base-x1 | 9 | 14 | 124.64 | 0.966 [0.377, 1.774] | 106.25 | 1.535 | 531.4 | 1065.4 | 0 | 0 |
| dev | 9 | 12 | 135.21 | 1.048 [1.001, 1.112] | 72.81 | 1.052 | 188.1 | 1005.9 | 0 | 0 |
| dts-v2-nodse | 9 | 12 | 129.05 | 1.000 [1.000, 1.000] | 69.23 | 1.000 | 175.9 | 1019.4 | 0 | 0 |
| dts-v3 | 9 | 13 | 125.34 | 0.971 [0.388, 1.721] | 88.47 | 1.530 | 420.6 | 1063.4 | 0 | 0 |
| dts-v4 | 9 | 12 | 134.37 | 1.041 [1.001, 1.094] | 73.87 | 1.067 | 175.0 | 1012.3 | 0 | 0 |

Contention: 0/90 runs ended with a local LLM server active.

Gate (ratio <= 0.97, CI upper < 1, no wrong answers, no crashes, solved >= control on paired runs): base-x1 no pass (speed), dev no pass (speed), dts-v3 no pass (speed), dts-v4 no pass (speed)

Reference coverage: 80/90 runs have a KNOWN OPTIMUM (=opt=, checked: bounds must bracket it, 'Optimal' must match it); 0 have only a best-known value (=best=, not checked); 10 have no reference. Unchecked runs are not evidence of correctness. Objective checks do not establish primal feasibility (see bench/solcheck.py).
Instances without a known optimum: neos-3402454-bohle

