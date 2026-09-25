# Option sweep (hard set) and v2-nodse identical check (2026-09-25 15:30–15:52)

## v2 without DSE vs dev — small set, seed 0, 120 s (`bench/results/2026-09-25-v2nodse-ident.md`)
SGM ratio **0.976 [0.954, 0.993]**, both-solved 0.971, solved 29 vs 28, **identical search 28/28**, 0 wrong, 0
crashed. Pure code speed-up (clique marking + find_common fix, symmetry dense hash, free wins, P1). Gate: no pass
(speed ≤ 0.97 not met; 33 instances are underpowered for a 3 % gate — decided on the night set, D-004 rule 1).

## Option sweep on dts-v2 — hard set, seed 0, 60 s (`bench/results/2026-09-25-opts-hard.md`; rerun of the invalid 15:12 set)
| option | ΔPDGI vs dts-v2 [95 % CI] | feasible (ctl 35) |
|---|---|---|
| mip_heuristic_run_zi_round | +0.0012 [−0.0023, +0.0047] | 35 |
| mip_heuristic_effort 0.1 | +0.0118 [−0.0034, +0.0398] | 34 |
| mip_heuristic_effort 0.2 | +0.0131 [−0.0052, +0.0435] | 33 |
| mip_heuristic_run_shifting | +0.0135 [−0.0067, +0.0454] | 34 |
None helps on hard instances at 60 s; all point slightly worse. O1 → rejected for now (60 s horizon only; a
300 s horizon could differ for heuristic effort).
