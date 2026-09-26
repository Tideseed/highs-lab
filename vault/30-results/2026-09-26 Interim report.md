# Interim report — HiGHS lab, 2026-09-26 afternoon (for reviewer feedback before the wrap-up)

**Goal.** Make HiGHS faster / better at closing MIP gaps on top of upstream `latest` (6293630a84, unchanged since
2026-09-25), measured honestly. North star: shifted geometric mean (shift 10 s) of solve time on the MIPLIB 2017
benchmark set (240), 300 s, 1 thread, `dev-tideseed` / `dev`, plus solved count and zero wrong answers.

**What is measured.** Clean run `2026-09-26-clean1` (both local LLM servers stopped, 10 pinned Cortex-X925 lanes,
8 GB per run, seed 0): stable v1.15.1 · dev (upstream latest) · **dev-tideseed v3** (4a7937f32e) · v3 with PGO.
Interim at 214 of 240 instances (all four arms paired). Seed 1 (dev vs v3) runs tonight 00:15; experiments freeze
tomorrow morning.

## Interim numbers (214 instances, seed 0)
| arm | SGM ratio vs dev [95 % CI] | both-solved | solved | ΔPDGI vs dev [CI] | wrong |
|---|---|---|---|---|---|
| stable v1.15.1 | 1.044 [1.008, 1.086] | 1.028 | 84 | +0.008 [−0.013, +0.028] | 0 |
| dev (latest) | 1 | 1 | 90 | 0 | 0 |
| **dev-tideseed v3** | **0.982 [0.935, 1.023]** | **0.951** | 88 | −0.006 [−0.013, +0.001] | 0 |
| v3 + PGO | 0.978 [0.933, 1.019] | 0.945 | 88 | −0.005 [−0.011, +0.001] | 0 |

- v3 is ~5 % faster where both solve; overall ratio 0.98 with a CI crossing 1 — **not yet a pass** of the gate
  (≤ 0.97, CI < 1). Solve flips vs dev: lost krka (seed luck, known), atrato, neos-873061 (dev 97 s — a real loss to
  diagnose), nexp-150-20-8-5, satellites2-60-fs, tbfp-network (dev 257–297 s, at the limit); won istanbul-no-cutoff,
  neos-662469, **neos-787933 (2 s; dev unsolved)**, rocI-4-11.
- PGO on the same source: identical search, ~0.3–3 % faster (0.997 overall here; 0.970 on the 33-instance screen).
- One v3 run on neos-3402454-bohle was killed by the harness's 8 GB per-run memory cap (8.4 GB; the same code with
  PGO peaked at 6.5 GB, dev at 1.7 GB) — counted as unsolved, not a code crash. neos-5114902-kasavu overruns the time
  limit by ~880 s in stable too (pre-existing).

## Branches in v3 and their evidence
| branch | what | evidence |
|---|---|---|
| clique-partition-marking (+ find_common fix) | clique neighbour queries by marking instead of pairwise hash-tree intersections; fixes a HighsHashTree::find_common false negative | s100: 172 s/no solution → 62 s/feasible at a 60 s limit; shadow-checked against pairwise on every call |
| symmetry-dense-hash | dense vertex hashes in symmetry refinement | chromaticindex: time after presolve 27.7 → 14.7 s; identical search |
| free-wins | skip unused glpsol errors after every LP; cache column maxima in presolve | 1–2 % of MIP time; identical search |
| presolve-changed-col (P1) | skip the markChangedCol column walk when no row is flagged | toguru presolve 12.5 → 6.2 s, same reductions; identical search 28/28 |
| dse-cache | restore dual steepest-edge weights of a recently used basis from a hash-keyed cache | 9 inst × 3 seeds: 0.959 [0.884, 1.049]; the cut-row "carry" half was measured and dropped (1.003) |
| dual-substitution-mirrored (X1, from the SCIP comparison) | HiGHS's dual substitution also in the mirrored orientation (x = y under a big-M row) | neos-787933 unsolved → 2–10 s (SCIP: 2.5 s); comp07-2idx faster 4/5 seeds; widden ~1.4× slower (3/3 at 900 s) |

v2 (without X1, with the DSE carry) vs dev on the small set: 0.976 [0.954, 0.993] with identical search 28/28 for the
no-DSE part.

## Tried and rejected
One-opt heuristic (never fired), locks heuristic (no effect after a crash fix), heuristic options (ZI round, shifting,
effort 0.1/0.2: no gain on the hard set), `-mcpu=native` (0 %), DSE cut-row carry (neutral, causes mas76 regression).

## Process issues found and fixed
Rebuild during a run (invalid set; run.py now hashes binary + libhighs before every job), HiGHS's own P-D integral
scoring "no bounds" as perfect (own PDGI), my 19:34 memwatch shed (run sets now memory-budgeted), query-count
mismatch in the clique change (search path changed; fixed and verified identical).

## Questions for reviewers
1. Is the north-star protocol (1 seed tonight + 1 today, 300 s, SGM shift 10 s, bootstrap over instances) adequate for
   a claim, or should the final report only claim the per-branch identical-search speed-ups?
2. X1 is a trade-off (one dramatic win, one consistent ~1.4× loss). Keep it in dev-tideseed, gate it by a structural
   criterion, or leave it out?
3. neos-873061 (dev 97 s, v3 unsolved at 300 s): worth a targeted look before the freeze, or leave as a documented
   loss?
4. Anything in the method or reporting that would make these numbers untrustworthy?
