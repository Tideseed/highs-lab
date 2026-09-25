---
id: X1
area: presolve
status: candidate
gate: full
effort: 1-2 d
verified_in_source: true
profiled_share: null
branch: null
---
# X1: Dual aggregation into variable upper bounds

**Where:** highs/presolve/HPresolve.cpp (no such rule; VUB detection exists at ~9722 for implications only)

**What:** SCIP setppc/dual presolve: a zero-cost binary x_j whose only up-lock is a big-M row sum x <= M y_i with |row| <= M (equivalent to x_j <= y_i) is aggregated x_j = y_i. neos-787933: SCIP 236376 -> 1764 vars, solved at the root in 2.5 s; HiGHS stops at 63708 cols, 22 % gap after 60 s (unsolved at 300 s).

**Proposed fix:** Detect VUB-equivalent rows (count/coef bound), then dual aggregation of columns whose only opposing lock is that VUB (Achterberg et al. 2020, dual aggregation).

**Source:** static read of `latest` on 2026-09-25 (checked by hand).
Measured share, branch and status: see frontmatter (kept current there only).

## Log
- 2026-09-25 filed from the codebase sweep.
