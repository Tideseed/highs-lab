# DRAFT — new issue ERGO-Code/HiGHS (not posted; needs Berk's yes)

Prior art searched 2026-09-25: "find_common", "HighsHashTree" (#2141 insert out-of-bounds, #2326 presolve behaviour —
unrelated), "cliquePartition". None.

**Title:** `HighsHashTree::find_common` can miss a common key when a leaf holds several entries with equal hashes

> Note: I am Claude Code (Anthropic's coding agent), filing this on behalf of Berk Orbay (@berkorbay). Per
> CONTRIBUTING.md this is a report, not a pull request.

**Description.** In `findCommonInLeaf` (leaf–leaf case, `highs/util/HighsHashTree.h` ~l. 533–553 on `latest`
6293630a84), when `leaf1->hashes[i] == leaf2->hashes[j]` but the keys differ, both `i` and `j` are advanced. The stored
hashes are per-level chunks, so different keys can share a stored hash; if leaf1 = [a, b] and leaf2 = [b, c] with
all four hashes equal, `a` is compared with `b`, then `b` with `c`, and the common key `b` is never compared. 
`find_common` then returns `nullptr` although both trees contain the key.

**Effect.** `HighsCliqueTable::findCommonCliqueId` reports "no common clique" for two literals that share one, so
clique separation (`bronKerboschRecurse`), clique partitioning and other neighbourhood queries miss neighbours. It does
not produce wrong solutions (a missed clique only weakens cuts/propagation), but it is silent.

**Observed on** MIPLIB 2017 `sorrell3` (threads=1): literals 199/1 and 72/1 are both linked to clique 149967 (length
31; `invertedHashList[...].contains(149967)` is true for both) while `find_common` returns `nullptr` in both argument
orders. Found by comparing `queryNeighbourhood` against an independent computation on every call.

**Suggested fix** (illustration: https://github.com/Tideseed/HiGHS/compare/latest...lab/hash-tree-find-common): on
equal hashes, compare the entry of leaf1 with every entry of leaf2 in the run of equal hashes, and advance only `i`.
With it, the independent computation and `find_common` agree on all calls in 10 MIPLIB instances; unit tests pass.
