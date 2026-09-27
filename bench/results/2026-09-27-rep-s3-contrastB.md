# Bench analysis: `/home/coulson/git_repositories/highs-lab/bench/results/raw/2026-09-27-rep-s3`

control = `dts-v2-nodse`, 720 runs, arms: dev, dts-v2-nodse, dts-v4

| arm | n inst | solved | SGM all (s) | ratio vs control [95% CI] | SGM both-solved | ratio | mean overrun (s) | max overrun (s) | wrong | crashed |
|---|---|---|---|---|---|---|---|---|---|---|
| dev | 240 | 93 | 137.76 | 1.007 [1.002, 1.013] | 34.50 | 1.020 | 8.0 | 902.5 | 0 | 0 |
| dts-v2-nodse | 240 | 96 | 136.74 | 1.000 [1.000, 1.000] | 36.41 | 1.000 | 8.0 | 791.1 | 0 | 1 |
| dts-v4 | 240 | 98 | 132.63 | 0.970 [0.949, 0.989] | 31.47 | 0.931 | 7.9 | 782.9 | 0 | 1 |

Contention: 0/720 runs ended with a local LLM server active.

Gate (ratio <= 0.97, CI upper < 1, no wrong answers, no crashes, solved >= control on paired runs): dev no pass (speed, fewer solved), dts-v4 no pass (1 crashed)

Reference coverage: 696/720 runs have a KNOWN OPTIMUM (=opt=, checked: bounds must bracket it, 'Optimal' must match it); 3 have only a best-known value (=best=, not checked); 21 have no reference. Unchecked runs are not evidence of correctness. Objective checks do not establish primal feasibility (see bench/solcheck.py).
Instances without a known optimum: bnatt500, cryptanalysiskb128n5obj14, fhnw-binpack4-4, neos-2075418-temuka, neos-3402454-bohle, neos-3988577-wolgan, neos859080, supportcase22

## Crashes / harness timeouts

- dts-v2-nodse neos-3402454-bohle s3 rc=-15 timeout=False
- dts-v4 neos-3402454-bohle s3 rc=-15 timeout=False

