---
id: S3
area: mip
status: candidate
gate: full (search path changes)
effort: 0.5-1 d
verified_in_source: true
profiled_share: null
branch: null
---
# S3: Propagate after every replayed change

**Where:** highs/mip/HighsDomain.cpp:2174,2203,2219 setDomainChangeStack

**What:** Installing a node calls propagate() after every stored bound change instead of once per branching level.

**Proposed fix:** Propagate once per branching level; keep conflict reasons.

**Source:** static read of `latest` on 2026-09-25 (checked by hand).
Measured share, branch and status: see frontmatter (kept current there only).

## Log
- 2026-09-25 filed from the codebase sweep.
