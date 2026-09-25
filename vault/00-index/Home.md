# highs-lab: Home

**Question:** how much faster can HiGHS become, and how much better can it close MIP gaps, with changes built on top of
upstream `latest`, measured honestly?

## Current state (2026-09-25 13:00)
| arm | source |
|---|---|
| `main` | upstream `master` 73cac48c53 (v1.15.1 line) |
| `dev` | upstream `latest` 6293630a84 |
| `dev-tideseed` | `dev` + lab/clique-partition-marking (incl. hash-tree fix) + lab/symmetry-dense-hash + lab/free-wins + lab/dse-carry-weights |

Screens so far (one seed, not yet the gate): see [[2026-09-25 Hard-set screens r2-r4]].
- Hard set (42, 60 s): dev-tideseed solved 1 / feasible 35 vs dev 0 / 33, mean gap 50.6 vs 54.4 %, worst overrun 33 s
  vs 251 s, 0 wrong, 0 crashes. neos-3004026-krka solved in ~20 s (DSE reuse); s100 feasible within its limit (C1).
- Small set (33 solved in 3–300 s, 120 s): neutral, ratio 1.011 [0.95, 1.08], 0 wrong; large per-instance spread
  both ways → attribution with 3 seeds running; full night benchmark pending Berk's OK on the window.
- Upstream-worthy: #3314 root cause (C1), find_common false negatives (C4), debug printf (P9).

## Start here
- [[Benchmark design]]: arms, instance sets, metrics, gate
- [[Sync and auto-resolution]]: how `dev-tideseed` stays on top of upstream
- [[Candidates]]: every inefficiency found so far and its status
- [[Upstream activity]]: what the HiGHS developers are working on (avoid duplicating)
- [[D-001 Patch queue on latest]], [[D-002 Build and benchmark windows]]
- Journal: `20-journal/`; results: `30-results/`; upstream drafts: `70-upstream/`

## Ground rules
No PRs upstream (HiGHS CONTRIBUTING: no AI-generated solver PRs); issues with evidence only, each approved by Berk.
Every claim is measured against `dev` in the same session.
