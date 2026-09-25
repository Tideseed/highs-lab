# Small set, 3 arms, 3 seeds (2026-09-25 14:48)

33 MIPLIB instances solved by HiGHS 1.15.1 in 3–300 s (`bench/sets/small51.txt`), 120 s limit, seeds 0–2, 1 thread,
X925 cores, Agent Fast up (idle). `bench/results/2026-09-25-3arm-small.md`.

| | stable v1.15.1 | dev (latest) | dev-tideseed (v1) |
|---|---|---|---|
| solved (of 99) | 80 | 82 | 82 |
| SGM ratio vs dev [95 % CI] | 0.985 [0.93, 1.04] | 1.000 | 0.965 [0.91, 1.02] |
| both-solved ratio | 0.988 | 1.000 | 0.956 |
| worst overrun | 9.8 s | 17.6 s | 1.7 s |
| wrong / crashed | 0 / 0 | 0 / 0 | 0 / 0 |

First north-star-type reading: ~3.5 % faster than latest, CI still touching 1. v1 = C1+C4, C3, C6+C7, C5 (DSE).
