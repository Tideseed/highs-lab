---
id: P8
area: presolve
status: candidate
gate: full (LP)
effort: 2 h
verified_in_source: false
profiled_share: null
branch: null
---
# P8: Dependent equations 100 s budget

**Where:** highs/presolve/HPresolve.cpp:7297

**What:** LP presolve may spend up to 100 s on the dependent-equations LU when no time limit is set.

**Proposed fix:** Budget scaled to equation nnz.

**Source:** static read of `latest` on 2026-09-25 (sweep agent, not yet checked by hand).
Measured share, branch and status: see frontmatter (kept current there only).

## Log
- 2026-09-25 filed from the codebase sweep.
