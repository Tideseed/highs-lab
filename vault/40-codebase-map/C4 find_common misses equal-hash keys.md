---
id: C4
area: util
status: branch
gate: full
effort: 1 h
verified_in_source: true
profiled_share: n/a (correctness)
branch: lab/hash-tree-find-common
---
# C4: find_common misses equal-hash keys

**Where:** highs/util/HighsHashTree.h:533-553 findCommonInLeaf (leaf-leaf merge)

**What:** Equal stored hashes with different keys advance both leaves, so a common key can be skipped: false 'no common clique' (sorrell3, clique 149967). Correctness bug: clique separation/partition miss neighbours.

**Proposed fix:** Compare each entry with all entries of the other leaf that have the same hash.

**Evidence so far:** static read of `latest` on 2026-09-25 (checked by hand).
Profile share: not measured yet.

## Log
- 2026-09-25 filed from the codebase sweep.
