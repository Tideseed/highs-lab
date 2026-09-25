---
id: L6
area: simplex
status: candidate
gate: identical
effort: 1 d
verified_in_source: false
profiled_share: null
branch: null
---
# L6: Branchy fused loops and per-rebuild HVectors

**Where:** HEkkDualRHS.cpp:327; HEkkDualRow.cpp:557; HEkk.cpp:2919,2954

**What:** Dense/sparse fused loops, aliasing reloads, HVector allocations per rebuild.

**Proposed fix:** Split loops, locals, member buffers.

**Source:** static read of `latest` on 2026-09-25 (sweep agent, not yet checked by hand).
Measured share, branch and status: see frontmatter (kept current there only).

## Log
- 2026-09-25 filed from the codebase sweep.
