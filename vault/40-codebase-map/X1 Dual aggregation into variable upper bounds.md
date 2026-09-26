---
id: X1
area: presolve
status: branch (mixed: diagnose losses)
gate: full
effort: 1-2 d
verified_in_source: true
profiled_share: n/a (presolve rule)
branch: lab/dual-substitution-mirrored
---
# X1: Dual aggregation into variable upper bounds

**Where:** highs/presolve/HPresolve.cpp (no such rule; VUB detection exists at ~9722 for implications only)

**What:** SCIP setppc/dual presolve: a zero-cost binary x_j whose only up-lock is a big-M row sum x <= M y_i with |row| <= M (equivalent to x_j <= y_i) is aggregated x_j = y_i. neos-787933: SCIP 236376 -> 1764 vars, solved at the root in 2.5 s; HiGHS stops at 63708 cols, 22 % gap after 60 s (unsolved at 300 s).

**Proposed fix:** Detect VUB-equivalent rows (count/coef bound), then dual aggregation of columns whose only opposing lock is that VUB (Achterberg et al. 2020, dual aggregation).

**Source:** static read of `latest` on 2026-09-25 (checked by hand).
Measured share, branch and status: see frontmatter (kept current there only).

## Log
- 2026-09-25 filed from the codebase sweep.
- 2026-09-25 evening: HiGHS already has this rule (dualFixing → substituteCol, Achterberg et al. 4.4 "dual
  substitution") but only in one orientation (x = 1 − y). Added the mirrored orientation (x = y), tried after the
  existing one so earlier reductions are unchanged. neos-787933: presolve 1897×236376 → 131×1213 (SCIP: 1764 vars),
  solved to optimality 30 in 2.5 s at the root (was unsolved at 300 s). Solution feasible against the original model
  (bench/solcheck.py), 101/101 unit tests. Branch c81725e48f. Next: reach scan over 240 instances, hard + small screens.
- 2026-09-26 night-lite: on its 27 affected instances SGM 0.938 [0.72,1.13], solved 21 vs 22; neos-787933 won, widden (2/2) and comp07-2idx (1/2) lost. Restrict before merging. See [[2026-09-26 Night-lite]].
