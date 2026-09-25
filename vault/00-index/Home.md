# highs-lab: Home

**Question:** how much faster can HiGHS become, and how much better can it close MIP gaps, with changes built on top of
upstream `latest`, measured honestly?

## Current state (update on every accepted, rejected or dropped branch)
| arm | source | last clean measurement |
|---|---|---|
| `main` | upstream `master` 73cac48c53 (v1.15.1 line) | none yet |
| `dev` | upstream `latest` 6293630a84 (2026-09-25) | none yet |
| `dev-tideseed` | = `dev` (no accepted branches yet) | none yet |

**Margin of dev-tideseed over dev:** not measured yet.

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
