# Bench analysis: `bench/results/raw/2026-09-26-dsm-changed`

control = `dev`, 108 runs, arms: dev, lab-dsm

| arm | n inst | solved | SGM all (s) | ratio vs control [95% CI] | SGM both-solved | ratio | mean overrun (s) | max overrun (s) | wrong | crashed |
|---|---|---|---|---|---|---|---|---|---|---|
| dev | 27 | 22 | 149.53 | 1.000 [1.000, 1.000] | 49.91 | 1.000 | 4.9 | 36.2 | 0 | 0 |
| lab-dsm | 27 | 21 | 140.22 | 0.938 [0.718, 1.130] | 40.66 | 1.001 | 3.7 | 33.0 | 0 | 0 |

Contention: 108/108 runs ended with a local LLM server active.

Gate (ratio <= 0.97, CI upper < 1, no wrong answers, no crashes, solved >= control on paired runs): lab-dsm no pass (speed, fewer solved)

Reference coverage: 104/108 runs have a known objective in solu.txt; the others cannot show a wrong answer and are not evidence of correctness.

