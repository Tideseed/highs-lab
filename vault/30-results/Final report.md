# HiGHS lab — final report (draft at the freeze, 2026-09-27 07:30; reviewer feedback pending)

**Question.** Can HiGHS be made faster, or better at closing MIP gaps, on top of upstream `latest`, in two days, with
honest measurement? Upstream `latest` = 6293630a84 throughout (no upstream commits during the project).

## Headline
- **dev-tideseed v4** (clique marking + find_common fix, symmetry dense hash, free wins, P1 presolve counter,
  DSE cache) vs latest, MIPLIB 2017 benchmark set (240), 300 s, 1 thread, clean window, **seed 1**:
  SGM **0.969 [0.939, 0.996]**, both-solved 0.933, solved **101 vs 98**, ΔPDGI **−0.010 [−0.019, −0.002]**, 0 wrong,
  0 crashed → **passes the gate on one seed; not replicated** (no v4 seed-0 run). The same branches plus X1 (v3) on
  seed 0: 0.985 [0.942, 1.022], solved 96 vs 99 — no pass. Read together: a small (~1–3 %) improvement, not yet
  established; the evidence leans positive for v4, negative for adding X1 to the combination.
- **Upstream progress, measured:** latest vs release v1.15.1 = 3.6 % faster on the full set (stable 1.036
  [1.001, 1.073]); ~25 % better PDGI on the 42 hard instances.
- **Local wins (identical search unless stated):** s100 (time-limit overrun 170 s → stops on time with a feasible
  solution), toguru presolve 12.5 → 6.2 s, chromaticindex −47 % after presolve, DSE cache −8 to −23 % on binkar10_1,
  roll3000, timtab1, seymour1 (search changes), neos-787933 unsolved → 3–5 s (X1, search changes).
- **Correctness:** a real HiGHS bug (HighsHashTree::find_common false negatives) with a fix; 0 wrong answers in all
  runs; 385 reported-optimal solutions of clean1 independently checked feasible against the original models.

## Branch status (Tideseed/HiGHS)
| branch | kind | status | evidence |
|---|---|---|---|
| lab/clique-partition-marking (+ find_common fix) | speed + correctness | in v4 | s100; sorrell3 clique separation; shadow-checked exact vs corrected pairwise |
| lab/hash-tree-find-common | correctness | reference (also inside the clique branch) | sorrell3 clique 149967 |
| lab/symmetry-dense-hash | speed, identical | in v4 | chromaticindex 27.7 → 14.7 s after presolve |
| lab/free-wins | speed, identical | in v4 | 1–2 % of MIP time; toguru 13 % |
| lab/presolve-changed-col (P1) | speed, identical | in v4 | toguru presolve −50 %; 28/28 identical |
| lab/dse-cache | speed, search changes | in v4 | 9 inst × 3 seeds 0.959; ablation neutral except csched008 s0 |
| lab/dual-substitution-mirrored (X1) | quality, search changes | experimental, OUT of the claim | neos-787933 win; losses on neos-873061, comp07 s1, widden |
| lab/dse-carry-weights | — | superseded (carry half dropped: 1.003) | DSE split |
| lab/one-opt, lab/locks-heuristic | quality | rejected (no effect) | screens |
| build: PGO | build | optional, NOT identical search (90/95) | 0.996 [0.991, 1.001] on clean1 |
| options sweep, -mcpu=native | — | rejected | no gain |

## What did not work, and why that is informative
Heuristics copied from SCIP (one-opt, locks) never fired: HiGHS's incumbents are already one-opt-optimal on the tried
instances and its existing sub-MIP heuristics cover the locks niche. Small screens overstated effects that shrank on
the full set (PGO 3 % → 0.4 %; v2 2.4 % → ~0.4 % outside X1's instances): hot-spot fixes do not move a 240-instance
geometric mean.

## Incidents and fixes (process)
Memory shed at 19:34 on 09-25 (run sets now memory-budgeted); a rebuild during a run (run.py hashes binary+lib before
every job); PDGI scored missing bounds and unlogged tails as good (own PDGI, tail fix after review); a query-count
mismatch changed a search path (fixed); my wrong attribution of kasavu (fixed after the ablation); a night job
resumed on a stopped server (script now restores before resuming). Reviews: #3, #4, #5.

## Open (not done before the freeze)
Replication of v4 on a second seed; neos-873061 is X1's clearest loss; kasavu/bohle time-limit leaks exist in latest
itself; per-branch paired tables for the identical-search branches (in progress for the report).
