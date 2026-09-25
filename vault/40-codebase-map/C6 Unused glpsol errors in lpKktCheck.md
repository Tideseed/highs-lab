---
id: C6
area: lp_data
status: branch
gate: identical
effort: 15 min
verified_in_source: true
profiled_share: 1-2% (neos5 1.9%)
branch: lab/free-wins
---
# C6: Unused glpsol errors in lpKktCheck

**Where:** highs/lp_data/HighsSolution.cpp:1175 lpKktCheck -> getLpKktFailures(&primal_dual_errors)

**What:** Glpsol-style errors computed after every LP solve (incl. MIP resolves) and never read: 1-2 % of MIP time.

**Proposed fix:** Pass nullptr; keep the basis check.

**Source:** static read of `latest` on 2026-09-25 (checked by hand).
Measured share, branch and status: see frontmatter (kept current there only).

## Log
- 2026-09-25 filed from the codebase sweep.
