# highs-lab: Home

**Question:** how much faster can HiGHS become, and how much better can it close MIP gaps, with changes built on top of
upstream `latest`, measured honestly?

## Current state
Arm composition and SHAs: `bench/COMPOSITION.md` (single source; do not repeat it here). Queue states: `bench/queue.txt`
(`merged` = in dev-tideseed for measurement, `accepted` = passed the gate). Decision rules: [[D-004 Decision rules for tonight]].
Latest results: `vault/30-results/` (newest first). Reviews: highs-lab #3 (Codex), #4 (Claude Code).

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
