# Bench analysis: `/home/coulson/git_repositories/highs-lab/bench/results/raw/2026-09-27-rep-pooled`

control = `dts-v2-nodse`, 1440 runs, arms: dev, dts-v2-nodse, dts-v4

| arm | n inst | solved | SGM all (s) | ratio vs control [95% CI] | SGM both-solved | ratio | mean overrun (s) | max overrun (s) | wrong | crashed |
|---|---|---|---|---|---|---|---|---|---|---|
| dev | 240 | 189 | 139.03 | 1.007 [1.002, 1.012] | 33.18 | 1.020 | 5.1 | 902.5 | 0 | 0 |
| dts-v2-nodse | 240 | 195 | 138.08 | 1.000 [1.000, 1.000] | 35.60 | 1.000 | 5.0 | 791.1 | 0 | 2 |
| dts-v4 | 240 | 196 | 135.43 | 0.981 [0.967, 0.994] | 32.00 | 0.959 | 4.6 | 782.9 | 0 | 2 |

Contention: 0/1440 runs ended with a local LLM server active.

Gate (ratio <= 0.97, CI upper < 1, no wrong answers, no crashes, solved >= control on paired runs): dev no pass (speed, fewer solved), dts-v4 no pass (speed, 2 crashed)

Reference coverage: 1392/1440 runs have a KNOWN OPTIMUM (=opt=, checked: bounds must bracket it, 'Optimal' must match it); 6 have only a best-known value (=best=, not checked); 42 have no reference. Unchecked runs are not evidence of correctness. Objective checks do not establish primal feasibility (see bench/solcheck.py).
Instances without a known optimum: bnatt500, cryptanalysiskb128n5obj14, fhnw-binpack4-4, neos-2075418-temuka, neos-3402454-bohle, neos-3988577-wolgan, neos859080, supportcase22

## Crashes / harness timeouts

- dts-v2-nodse neos-3402454-bohle s3 rc=-15 timeout=False
- dts-v4 neos-3402454-bohle s3 rc=-15 timeout=False
- dts-v2-nodse neos-3402454-bohle s2 rc=-15 timeout=False
- dts-v4 neos-3402454-bohle s2 rc=-15 timeout=False

