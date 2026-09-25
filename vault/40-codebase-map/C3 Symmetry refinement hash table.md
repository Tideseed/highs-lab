---
id: C3
area: presolve
status: gated-quick
gate: identical
effort: 2 h
verified_in_source: true
profiled_share: 17.7% chromaticindex
branch: lab/symmetry-dense-hash
---
# C3: Symmetry refinement hash table

**Where:** highs/presolve/HighsSymmetry.h:200 vertexHash (HighsHashTable<HighsInt,u32>), HighsSymmetry.cpp:735,755,824-936

**What:** Hash table keyed by vertex, updated per edge during partition refinement and cleared (shrunk) per refinement: 17.7 % self on chromaticindex1024-7.

**Proposed fix:** Dense array + flag + touched list (same semantics).

**Evidence so far:** static read of `latest` on 2026-09-25 (checked by hand).
Profile share: not measured yet.

## Log
- 2026-09-25 filed from the codebase sweep.
