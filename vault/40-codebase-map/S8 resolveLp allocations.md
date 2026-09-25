---
id: S8
area: mip
status: candidate
gate: identical (hash) / check (objective)
effort: 2 h
verified_in_source: false
profiled_share: null
branch: null
---
# S8: resolveLp allocations

**Where:** highs/mip/HighsLpRelaxation.cpp:1455, 1621

**What:** New HighsHashTable per resolve; full-column CDouble objective sum.

**Proposed fix:** Member + clear(); objective from solver info.

**Source:** static read of `latest` on 2026-09-25 (sweep agent, not yet checked by hand).
Measured share, branch and status: see frontmatter (kept current there only).

## Log
- 2026-09-25 filed from the codebase sweep.
