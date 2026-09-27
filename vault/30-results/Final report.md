# HiGHS lab — final report (at the freeze, 2026-09-27; second review on #5 addressed 08:xx from existing data, no new runs)

**Question.** Can HiGHS be made faster, or better at closing MIP gaps, on top of upstream `latest`, in two days, with
honest measurement? Upstream `latest` = 6293630a84 throughout (no upstream commits during the project).

## Headline
- **dev-tideseed v4** (clique marking + find_common fix, symmetry dense hash, free wins, P1 presolve counter,
  DSE cache) vs latest, MIPLIB 2017 benchmark set (240), 300 s, 1 thread, clean window, **seed 1**:
  SGM **0.969 [0.939, 0.996]**, both-solved 0.933, solved **101 vs 98**, ΔPDGI **−0.010 [−0.019, −0.002]**, 0 wrong,
  0 crashed → **passes the gate on one seed; not replicated** (no v4 seed-0 run). The same branches plus X1 (v3) on
  seed 0: 0.985 [0.942, 1.022], solved 96 vs 99 — no pass.
- **How much one seed carries** (review #5, recomputed): dev against itself, seed 1 vs seed 0, same binary, both clean
  windows = **1.028**, and 92 of 240 instances move by more than 5 % — the control drifts by the size of the claimed
  effect. On the 213 instances outside X1's known set, v3 on seed 0 gives 0.999 and v4 on seed 1 gives 0.973. In favour
  of seed 1: the paired sign test is positive (38 faster by >5 %, 19 slower, p = 0.016), so the win is broad.
  **Truthful sentence: a 0–3 % effect, sign positive on the better-powered seed, not established.**
- **Where the seed-1 gain sits:** both solved on an identical path (the four deterministic branches' pure speed) 24
  instances, 0.961; both solved on a different path (dse-cache perturbs the search on 70 of 94) 0.925; not both solved
  146, 0.986. Most of the 3 % is path perturbation, the least replicable kind (krka 181 → 15 s; pg5_34 122 → 225 s).
- **Primal side (MIPFEAS-style primal integral, Mittelmann's metric, on the same runs):** v4 vs dev **0.960 [0.913,
  1.010]**, runs within 1 % of the reference by 300 s 155 vs 148; v3 vs dev on seed 0 0.959 [0.918, 1.001]; stable vs dev
  **1.165 [1.076, 1.273]**. Not established for v4 (CI crosses 1). See `2026-09-27 MIPFEAS-style primal integral.md`.
- **Upstream progress, measured:** latest vs release v1.15.1 = 3.6 % faster on the full set (stable 1.036
  [1.001, 1.073]); on the 42 hard instances PDGI 0.605 vs 0.654, ΔPDGI −0.049 [−0.103, −0.008] for latest (~8 %
  relative; an earlier "~25 %" came from HiGHS's own P-D integral, the metric this lab replaced); MIPFEAS-style primal
  integral 14 % better for latest (1/1.165).
- **Local wins (identical search unless stated):** s100 (at a 60 s limit: overrun 170 s → stops on time with a feasible solution; at 300 s neither
  latest nor v4 finds an incumbent, v4 leaves the root at 23 s instead of 176 s), **bohle presolve 349 s (limit hit in probing) → ~50 s with P1 alone**, same reductions, so the solver
  reaches the LP (single-branch builds, review #5), toguru presolve 12.5 → 6.2 s, chromaticindex −47 % after presolve, DSE cache −8 to −23 % on binkar10_1,
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
| lab/presolve-changed-col (P1) | speed, identical | in v4 | bohle presolve 349 → ~50 s; toguru presolve −50 %; 28/28 identical |
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
1. **Replicate v4 on seed 0 first** — one arm, 240 runs, ~2 h in a clean window; the clean1 dev seed-0 control exists:
   `box-window claim ...` then
   `bench/run.py --arms bench/arms.toml --only-arms dts-v4 --set bench/sets/miplib-bench-all.txt --seeds 0 --time-limit 300 --mem-reserve-gb 20 --out bench/results/raw/2026-09-26-clean1`
   and `bench/analyze.py bench/results/raw/2026-09-26-clean1 --control dev`. This settles the headline.
2. dse-cache's net sign (see its row); if negative, v4 minus dse-cache is the claim candidate (identical-path only).
3. **kasavu on latest itself:** seed-dependent time-limit leak at the root (dev seed 1 runs to ~1,300 s at a 300 s
   limit) — upstream-worthy on its own, evidence = the two seeds + the latest binary. Not filed (Berk: no issues yet).
4. neos-873061 is X1's clearest loss.
5. **Primal heuristics:** latest finds no incumbent by 300 s on 25/233 feasible instances (seed 1; list in the MIPFEAS
   note) and v4 does not change that count — MIPFEAS (600 s, 24 threads) has HiGHS 1.15.1 at 214/233 feasible, 4th of
   the open solvers on the primal integral although it proves the most optima (107). The natural next iteration.

## Memory on bohle is a phase effect, not a branch (review #5)
Every build that leaves presolve on this 2.9M-row model reaches ~6 GB in the LP; builds that stay in probing until the
limit peak at 1.6 GB (lab-cpm/sym/fw 1.6 GB, lab-pcc 6.1 GB). The seed-0 v3 OOM at the 8 GB cap was v3 reaching the LP
with a slightly larger footprint. Build provenance: `highs-builds/lab-sym`, `lab-fw`, `lab-pcc` print git hash
6293630a84 (configured before their branch commit existed); their source dir is the branch worktree, so the code is the
branch — rebuild before citing their banners.

## PDGI coverage
In clean2, 124 of 480 runs have their last progress row more than 60 s before the end, so a quarter of the ΔPDGI
(−0.010 [−0.019, −0.002]) is carried by the final bound appended at the end time. Quote it with that qualifier.

## Per-branch evidence for the identical-search branches (from existing data; reviewers' request)
**base** = clique marking + symmetry dense hash + free wins + P1 (dts-v2-nodse, 23395de1c6) vs dev, ablation of clean2
(clean window, 300 s, 2 seeds): **identical search on 12/12 both-solved runs** (same nodes and LP iterations). Timing on
identical paths (pure speed):
| instance | dev (s0, s1) | base (s0, s1) | note |
|---|---|---|---|
| neos-4722843-widden | 164.0, 165.6 | **112.8, 146.6** | −31 %, −11 %: one run per seed, noise floor ±12 % |
| neos-3402454-bohle | 348.9, 340.1 (overrun) | **300.3, 300.0** (stops on time) | unsolved both |
| neos-873061 | 98.8, 236.7 | 96.6, 227.8 | −2 %, −4 % |
| comp07-2idx, csched008, n5-3, kasavu, neos-787933 | | | within ±3 % |
| unitcal_7 | 38.5, 47.0 | 43.5, 42.6 | +12 %, −9 %: the timing noise floor on identical paths |
Earlier identical-search evidence: small set 28/28 (v2-nodse vs dev, 2026-09-25); targeted: s100 (60 s limit: 172 s,
no solution → 62 s, feasible), toguru presolve 12.5 → 6.2 s, chromaticindex after presolve 27.7 → 14.7 s (A725, single
runs). Timing differences within ±12 % on identical paths are noise at n = 1–2.
