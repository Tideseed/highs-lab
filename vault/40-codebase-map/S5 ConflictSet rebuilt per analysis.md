---
id: S5
area: mip
status: candidate
gate: identical
effort: 1 d
verified_in_source: false
profiled_share: null
branch: null
---
# S5: ConflictSet rebuilt per analysis

**Where:** highs/mip/HighsDomain.cpp:2585+, 3823; HighsRedcostFixing.cpp:151

**What:** Two std::set plus buffers built per conflict analysis; up to 100 back-to-back calls.

**Proposed fix:** Reusable workspace; vector frontier indexed by pos.

**Source:** static read of `latest` on 2026-09-25 (sweep agent, not yet checked by hand).
Measured share, branch and status: see frontmatter (kept current there only).

## Log
- 2026-09-25 filed from the codebase sweep.
