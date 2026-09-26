# Night-lite 2026-09-26 00:15–02:23 (servers up, halit paused; Agent Fast idle; Think off)

## Hard set, dev vs dts-v2 vs dts-v2-nodse (42, 60 s, seed 0) — `bench/results/2026-09-26-hard-v2.md`
dts-v2 ΔPDGI −0.011 [−0.042, +0.008], feasible 35 vs 33, solved 1 vs 0, worst overrun 13.6 s vs 279 s.
dts-v2-nodse ΔPDGI +0.0004 [−0.0049, +0.0077], feasible 34. v2 − nodse difference driven by neos-3004026-krka
(−0.565). D-004 rule 2 (DSE): not met (CI vs nodse includes 0) — undecided, as expected from one seed.

## X1 on its 27 affected instances, dev vs lab-dsm (300 s, seeds 0–1) — `bench/results/2026-09-26-dsm-changed*.md`
SGM 0.938 [0.718, 1.130], solved 21 vs 22, ΔPDGI +0.006 [−0.020, +0.027], 0 wrong, 0 crashed.
Wins: neos-787933 unsolved → 10.2 / 7.4 s. Losses: neos-4722843-widden solved by dev at 240/288 s, not by X1 (both
seeds); comp07-2idx s1 48 s → unsolved; slower n5-3 s0 (10.6 → 15.6 s), unitcal_7 s1 (64 → 95 s).
Verdict: not mergeable as is — the extra reductions change presolve paths elsewhere. Next: diagnose widden/comp07
(which reductions differ, what they remove), then restrict the rule (e.g. only when it eliminates a large share of
columns) and re-test the same 27.
