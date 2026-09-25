---
id: L5
area: simplex
status: candidate
gate: identical?
effort: 2-4 h
verified_in_source: false
profiled_share: null
branch: null
---
# L5: PRICE computes basic columns

**Where:** highs/util/HighsSparseMatrix.cpp:1423; HEkk.cpp:2889

**What:** Column-wise PRICE computes then zeroes basic columns; the zeros stay in the index list.

**Proposed fix:** Skip basic columns.

**Evidence so far:** static read of `latest` on 2026-09-25 (sweep agent, not yet checked by hand).
Profile share: not measured yet.

## Log
- 2026-09-25 filed from the codebase sweep.
