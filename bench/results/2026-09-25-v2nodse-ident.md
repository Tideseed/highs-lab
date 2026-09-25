# Bench analysis: `bench/results/raw/2026-09-25-v2nodse-ident`

control = `dev`, 66 runs, arms: dev, dts-v2-nodse

| arm | n inst | solved | SGM all (s) | ratio vs control [95% CI] | SGM both-solved | ratio | mean overrun (s) | max overrun (s) | wrong | crashed |
|---|---|---|---|---|---|---|---|---|---|---|
| dev | 33 | 28 | 33.29 | 1.000 [1.000, 1.000] | 25.53 | 1.000 | 1.0 | 4.7 | 0 | 0 |
| dts-v2-nodse | 33 | 29 | 32.49 | 0.976 [0.954, 0.993] | 24.80 | 0.971 | 0.3 | 1.0 | 0 | 0 |

Gate (ratio <= 0.97, CI upper < 1, no wrong answers, no crashes, solved >= control on paired runs, identical search): dts-v2-nodse no pass (speed)

Reference coverage: 66/66 runs have a known objective in solu.txt; the others cannot show a wrong answer and are not evidence of correctness.

## Identical-search check (both solved)

**dts-v2-nodse**: 28/28 identical

