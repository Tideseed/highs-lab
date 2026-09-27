# HiGHS lab — final report (frozen snapshot 2026-09-27; reviews on #5 addressed; replication D-006 running — results will be appended, not merged in)

**Question.** Can HiGHS be made faster, or better at closing MIP gaps, on top of upstream `latest`, in two days, with
honest measurement? Upstream `latest` = 6293630a84 throughout (no upstream commits during the project).

## Headline
- **dev-tideseed v4** (clique marking + find_common fix, symmetry dense hash, free wins, P1 presolve counter,
  DSE cache) vs latest, MIPLIB 2017 benchmark set (240), 300 s, 1 thread, clean window, **seed 1**:
  SGM **0.969 [0.939, 0.996]**, both-solved 0.933, solved **101 vs 98**, ΔPDGI **−0.010 [−0.019, −0.002]**, 0 wrong,
  0 crashed → **passes the gate on one seed; not replicated** (no v4 seed-0 run). The same branches plus X1 (v3) on
  seed 0: 0.985 [0.942, 1.022], solved 96 vs 99 — no pass.
- **Result as measured:** seed-1 SGM ratio 0.969 [0.939, 0.996] (a 0.4–6.1 % reduction of this SGM on this paired
  comparison), 101 vs 98 solved; **generalisation across seeds unestablished.** The instance bootstrap does not
  capture seed-to-seed uncertainty.
- **Sensitivity, exploratory** (review #5): dev against itself, seed 1 vs seed 0, same binary, different clean
  windows = **1.028**, and 92 of 240 instances move by more than 5 % (raw times; 77 on the shifted t+10 s times the SGM
  uses). This changes seed AND window, so it shows sensitivity; it does not invalidate the within-window paired
  result. v3 on seed 0 restricted to the 213 instances outside X1's *known* set gives 0.999 (v4 on seed 1, same
  instances: 0.973); X1's reach beyond the known set is unmeasured, so this is not a v4 replication. Paired sign test
  on seed 1: 38 faster by >5 %, 19 slower, p = 0.016.
- **Descriptive split of seed 1** (identical = same node and LP-iteration totals, the lab's operational check, not a
  proof of an identical internal path): both solved, identical totals 24 instances, 0.961; both solved, different
  totals 70, 0.925; not both solved 146, 0.986. DSE cache is the only branch meant to change the search, but the
  clique branch also carries a correctness fix, so the 70 are not all attributed to DSE (krka 181 → 15 s; pg5_34
  122 → 225 s).
- **Primal side (MIPFEAS-style primal integral, Mittelmann's metric, on the same runs):** v4 vs dev **0.960 [0.913,
  1.010]**, runs within 1 % of the reference by 300 s 155 vs 148 (estimates from sparse log rows); v3 vs dev on seed 0 0.959 [0.918, 1.001]; stable vs dev
  **1.165 [1.076, 1.273]**. Not established for v4 (CI crosses 1). See `2026-09-27 MIPFEAS-style primal integral.md`.
- **Upstream progress, measured:** latest vs release v1.15.1 = 3.6 % faster on the full set (stable 1.036
  [1.001, 1.073]); on the 42 hard instances PDGI 0.605 vs 0.654, ΔPDGI −0.049 [−0.103, −0.008] for latest (~8 %
  relative; an earlier "~25 %" came from HiGHS's own P-D integral, the metric this lab replaced); MIPFEAS-style primal
  integral 14 % better for latest (1/1.165).
- **Local wins (identical search unless stated):** s100 (at a 60 s limit: overrun 170 s → stops on time with a feasible solution; at 300 s neither
  latest nor v4 finds an incumbent, v4 leaves the root at 23 s instead of 176 s), **bohle**: dev spends 349 s in presolve (limit hit in probing, X925,
  clean run); a P1-only build finished presolve in 78 s (A725, single diagnostic run, review #5) and the combined base
  in 48.7 s (X925), same reductions, then reached the LP, toguru presolve 12.5 → 6.2 s, chromaticindex −47 % after presolve, DSE cache −8 to −23 % on binkar10_1,
  roll3000, timtab1, seymour1 (search changes), neos-787933 unsolved → 3–5 s (X1, search changes).
- **Correctness:** a real HiGHS bug (HighsHashTree::find_common false negatives) with a fix; 0 wrong answers in all
  runs; every saved incumbent of clean1, clean2 and D-006 seed 2 (1,865) rechecked with a fixed, locally-scaled
  checker: all feasible except two tolerance-edge rows on rocI-4-11 (see "Saved-solution recheck").

## Branch status (Tideseed/HiGHS)
| branch | kind | status | evidence |
|---|---|---|---|
| lab/clique-partition-marking (+ find_common fix) | speed + correctness | in v4 | s100; sorrell3 clique separation; shadow-checked exact vs corrected pairwise |
| lab/hash-tree-find-common | correctness | reference (also inside the clique branch) | sorrell3 clique 149967 |
| lab/symmetry-dense-hash | speed, identical | in v4 | chromaticindex 27.7 → 14.7 s after presolve |
| lab/free-wins | speed, identical | in v4 | 1–2 % of MIP time; toguru 13 % |
| lab/presolve-changed-col (P1) | speed, identical | in v4 | bohle presolve 349 s (dev, X925) vs 78 s (P1 only, A725, 1 run); toguru presolve −50 %; 28/28 identical |
| lab/dse-cache | speed, search changes | in v4, **net sign unestablished** | dse9 (selected where DSE recompute was expensive) 0.959, CI crosses 1; ablation (loss-selected) v4 vs base 1.041 [1.001, 1.094]: widden s0 113 → 168 s, csched008 s0 177 → 216, neos-873061 s0 97 → 116 |
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
1. **Replication with fresh controls — pre-registered as D-006** (review #5: a historical control breaks AGENTS.md
   rule 2): three arms dev / base / base+DSE in the same window, seeds 2 and 3 fixed in advance, new result
   directories, pinned binaries, shuffled run order, decision and stopping rules written before the first job.
   Seed 2 started 2026-09-27 09:14 on Berk's go-ahead. It strengthens or weakens the evidence; it does not by itself
   "settle" a population effect.
2. dse-cache's net sign: contrast B of D-006.
3. **kasavu on latest itself:** seed-dependent time-limit leak at the root (dev seed 1 runs to ~1,300 s at a 300 s
   limit) — upstream-worthy on its own, evidence = the two seeds + the latest binary. Not filed (Berk: no issues yet).
4. neos-873061 is X1's clearest loss.
5. **First upstream candidate, if Berk approves any filing:** the `find_common` correctness fix alone, with a
   minimal reproducer, a regression test and the invariant it restores, kept separate from the marking optimisation
   (Codex addendum). Its value does not depend on an aggregate speed-up. Subject to prior-art search and Berk's per-post yes.
6. **Primal heuristics:** latest finds no incumbent by 300 s on 25/233 feasible instances (seed 1; list in the MIPFEAS
   note) and v4 does not change that count — MIPFEAS (600 s, 24 threads) has HiGHS 1.15.1 at 214/233 feasible, 4th of
   the open solvers on the primal integral although it proves the most optima (107). The natural next iteration.

## Saved-solution recheck (fixed checker, local tolerances: row and bound 1e-6 relative to their own magnitude, integrality 1e-5)
| run set | runs | with a final incumbent | missing / unparsable files | checked | feasible | beyond tolerance | objective mismatches |
|---|---|---|---|---|---|---|---|
| clean1 (seed 0) | 960 | 826 | 0 / 0 | 826 | 825 | 1 | 0 |
| clean2 (seed 1) | 480 | 416 | 0 / 0 | 416 | 415 | 1 | 0 |
| D-006 seed 2 | 720 | 623 | 0 / 0 | 623 | 623 | 0 | 0 |

Both "beyond tolerance" cases are rocI-4-11 (stable s0, v4 s1): one row residual of exactly 1.0e-6 on a row of
magnitude 1 (1.00000000003e-6 and 1.00000000014e-6), i.e. at HiGHS's own primal feasibility tolerance, exceeding the
checker's equal tolerance only by floating-point rounding. Reported as tolerance-edge, not as infeasible solutions;
the tolerance was not changed after seeing them. Coverage gap: runs without a final incumbent (134 / 64 / 97) have
nothing to check; no solution file was missing. Worst values elsewhere: row 7.6e-7, bound 6.1e-7, integrality 8.7e-7.
This replaces the earlier "385 checked" claim.

## Memory on bohle (review #5)
Builds that leave presolve on this 2.9M-row model reached ~6 GB in the LP (lab-pcc 6.1 GB, base 6.4 GB); builds that
stay in probing until the limit peak at 1.6 GB (lab-cpm/sym/fw). The phase transition is a plausible explanation for
most of the increase, and the kernel log settles the seed-0 v3 OOM as an 8 GB-cap kill, not a crash; it does not prove
that branch-dependent memory overhead is absent. Build provenance: `highs-builds/lab-sym`, `lab-fw`, `lab-pcc` print git
hash 6293630a84 (configured before their branch commit existed). Their CMake source dir is the branch worktree, but that
alone does not prove which revision was compiled into the existing binary and there is no build manifest; the
provenance of those three diagnostic builds stays uncertain (no rebuild during the freeze).

## PDGI and primal-integral estimates
Both are computed from sparse logged rows: changes between rows are not observed, and the bootstrap does not quantify
that measurement error. In clean2, 124 of 480 runs have their last progress row more than 60 s before the end; that is a
coverage statistic. The final bound is appended at the run's completion time (never applied backward over the
unlogged tail), so an optimum proven late counts only from then — regression test `bench/tests/test_checkers.py`
(gap 0.5 from t=0, optimum at t=80, T=100 → 0.4). "Incumbent by T" and "feasible at termination" are now separate
columns in hard.py and primal.py; on the saved records of clean1 and clean2 they coincide for every arm.

## Per-branch evidence for the identical-search branches (from existing data; reviewers' request)
**base** = clique marking + symmetry dense hash + free wins + P1 (dts-v2-nodse, 23395de1c6) vs dev, ablation of clean2
(clean window, 300 s, 2 seeds): **identical search on 12/12 both-solved runs** (same nodes and LP iterations). Timing on
identical paths (pure speed):
| instance | dev (s0, s1) | base (s0, s1) | note |
|---|---|---|---|
| neos-4722843-widden | 164.0, 165.6 | **112.8, 146.6** | −31 %, −11 %: one run per seed |
| neos-3402454-bohle | 348.9, 340.1 (overrun) | **300.3, 300.0** (stops on time) | unsolved both |
| neos-873061 | 98.8, 236.7 | 96.6, 227.8 | −2 %, −4 % |
| comp07-2idx, csched008, n5-3, kasavu, neos-787933 | | | within ±3 % |
| unitcal_7 | 38.5, 47.0 | 43.5, 42.6 | +12 %, −9 %: observed variation on an identical path (two seeds) |
Earlier identical-search evidence: small set 28/28 (v2-nodse vs dev, 2026-09-25); targeted: s100 (60 s limit: 172 s,
no solution → 62 s, feasible), toguru presolve 12.5 → 6.2 s, chromaticindex after presolve 27.7 → 14.7 s (A725, single
runs). unitcal_7 varied by +12 % / −9 % between runs on an identical path; that is one instance's observed variation, not
a general noise floor, so small single-run differences are reported as observed, not declared noise.

## Appended after the freeze: D-006 replication (pre-registered; results appended, not merged into the text above)
- **Seed 2** (2026-09-27 09:14–13:35): base vs dev 0.995 [0.990, 1.002]; v4 vs base 0.995 [0.973, 1.016]; v4 vs dev
  0.990 [0.967, 1.011]; 0 wrong; 1 cap kill each for base and v4 (bohle, 8 GiB). No contrast passes; the seed-1 gain
  is not repeated on seed 2. `2026-09-27 D-006 seed 2.md`.
- **Seed 3** (14:06–18:30): base vs dev 0.993 [0.987, 0.998]; v4 vs base 0.970 [0.949, 0.989]; v4 vs dev 0.963 [0.941, 0.983].
- **Pooled seeds 2+3:** base vs dev **0.993 [0.988, 0.998]**; v4 vs base **0.981 [0.967, 0.994]**; v4 vs dev **0.974
  [0.959, 0.988]**; 0 wrong; bohle cap kills for base and v4 on both seeds. Registered decisions: A → no established
  aggregate effect; B → DSE dropped (crash condition; the crashes occur identically in base). Across seeds 1–3 v4 vs dev
  is 0.969 / 0.990 / 0.963: a ~2.5 % effect, below the 3 % gate. `2026-09-27 D-006 outcome.md`.
- Saved-solution recheck seed 3: 632/632 feasible (all four run sets: 2,497 incumbents, two tolerance-edge rows).
- **dev-tideseed = base** since 2026-09-27 19:0x (Berk followed the registered verdict); v4 remains as tag/branch.
