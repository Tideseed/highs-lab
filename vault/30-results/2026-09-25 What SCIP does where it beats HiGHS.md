# What SCIP does where it beats HiGHS (2026-09-25 evening; Berk's idea: learn from SCIP)

Source: optopt runs300 (MIPLIB, 80 instances, 300 s, 1 thread): HiGHS 1.15.1 vs SCIP (S0) are close overall — SGM
time HiGHS/SCIP 0.973, solved 38 vs 32 — but complementary. SCIP 10.0 (pyscipopt 6.2.1) re-run with full statistics
on the 12 instances where it wins most (`bench/scip-diag/`, A725 cores, 300 s): all 12 solved.

| instance | HiGHS (300 s) | SCIP | what did the work in SCIP |
|---|---|---|---|
| neos-787933 | 3 % gap | 2.5 s, root | dualfix 172 668 + **setppc dual aggregation 61 944** → 1 764 vars; oneopt |
| neos-3004026-krka | no solution | 112 s | setppc presolve 8 580; zerohalf 5 836, flowcover 2 997, strongcg 2 910 |
| CMS750_4 | 58 % gap | 220 s, root | gomory 41k, cmir 12.6k, **flowcover 3.5k**; crossover, alns, adaptivediving |
| istanbul-no-cutoff | unsolved | 143 s | probing 14k; cmir 10.8k, flowcover 2k; adaptive/conflict/frac diving |
| cbs-cta | 59 s | 25 s, root | dualsparsify; cmir 1.1k, flowcover 417, mcf; rens, intshifting, locks |
| rail507 | unsolved | 149 s | logicor 267k, **domcol 42k**; zerohalf (only cuts); alns, oneopt, locks |
| seymour1, pk1, cod105, mas76, piperout-27, enlight_hard | 1.8–3× slower | | gomory/zerohalf/strongcg, clique cuts, locks/shifting/feaspump/diving |

Across the 12: best-solution heuristics — LP 7, **locks 5**, rens 4, clique 4, shifting 4, feaspump 3, **oneopt 3**,
pscostdiving 3; separators — gomory 9, cmir 8, **flowcover 7, zerohalf 7**, knapsackcover 6, impliedbounds 6.
Candidates X1–X6 filed in [[Candidates]]. Ranking by (evidence × breadth) / effort: X1 (one instance from
unsolved to root-solved; pattern = big-M/facility structure, common), X2 one-opt (cheap), X3 locks, X5 (analysis only
first), X4 flow cover, X6 diving/LNS. Re-implement ideas from the literature, never copy SCIP code (Apache-2.0 vs MIT).
