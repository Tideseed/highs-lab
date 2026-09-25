---
id: S1
area: mip
status: candidate
gate: identical
effort: 1-2 h
verified_in_source: true
profiled_share: null
branch: null
---
# S1: propagate allocates 2 x nnz buffer per call

**Where:** highs/mip/HighsDomain.cpp ~2378-2386

**What:** `std::unique_ptr<HighsDomainChange[]> changedbounds(new HighsDomainChange[2*nnz(A)])` on every propagate() with pending rows: several times per node, per strong-branching candidate, per replayed bound change. POD type, so malloc only, but multi-MB means mmap/munmap and page faults.

**Proposed fix:** Per-domain member buffer, grow-only.

**Evidence so far:** static read of `latest` on 2026-09-25 (checked by hand).
Profile share: not measured yet.

## Log
- 2026-09-25 filed from the codebase sweep.
