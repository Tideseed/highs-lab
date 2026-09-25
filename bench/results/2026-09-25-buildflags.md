# Bench analysis: `bench/results/raw/2026-09-25-buildflags`

control = `dev-tideseed`, 198 runs, arms: dev-tideseed, dts-native, dts-pgo

| arm | n inst | solved | SGM all (s) | ratio vs control [95% CI] | SGM both-solved | ratio | mean overrun (s) | max overrun (s) | wrong | crashed |
|---|---|---|---|---|---|---|---|---|---|---|
| dev-tideseed | 33 | 56 | 34.21 | 1.000 [1.000, 1.000] | 26.46 | 1.000 | 0.5 | 1.3 | 0 | 0 |
| dts-native | 33 | 56 | 34.35 | 1.004 [0.992, 1.018] | 26.60 | 1.005 | 0.6 | 1.6 | 0 | 0 |
| dts-pgo | 33 | 56 | 33.19 | 0.970 [0.949, 0.989] | 25.42 | 0.961 | 1.6 | 10.9 | 0 | 0 |

Gate (ratio <= 0.97, CI upper < 1, no wrong answers, solved >= control): dts-native no pass, dts-pgo no pass

## Identical-search check (both solved)

**dts-native**: 56/56 identical

**dts-pgo**: 56/56 identical

