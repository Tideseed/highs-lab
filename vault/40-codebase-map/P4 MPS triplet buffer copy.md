---
id: P4
area: io
status: candidate
gate: identical model
effort: 2 h
verified_in_source: false
profiled_share: null
branch: null
---
# P4: MPS triplet buffer copy

**Where:** highs/io/HMpsFF.cpp:766, 854, 147

**What:** Unreserved triplet vector copied again with .at().

**Proposed fix:** Append straight into CSC.

**Source:** static read of `latest` on 2026-09-25 (sweep agent, not yet checked by hand).
Measured share, branch and status: see frontmatter (kept current there only).

## Log
- 2026-09-25 filed from the codebase sweep.
