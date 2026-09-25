---
name: highs-sync
description: Sync the HiGHS fork with upstream latest, rebase lab branches (auto-resolving conflicts under gates), regenerate dev-tideseed, build and smoke-test the three arms. Use when asked to sync, rebase on latest, update dev-tideseed, or when the daily highs-sync reported a problem.
---
# Sync with upstream

The daily timer runs `scripts/highs-sync`; this is the same procedure by hand. Design: `vault/10-design/Sync and auto-resolution.md`.

1. Fetch: `git -C ~/git_repositories/highs fetch upstream latest master`.
2. **Rebase** each non-parked branch in `bench/queue.txt` onto `upstream/latest`. `rerere` is enabled.
3. **On a conflict:** resolve it in the branch's worktree.
   - Keep upstream's new behaviour and re-apply the branch's intent from its queue line.
   - If upstream now implements the same thing, drop the branch (status `dropped` in its note, with the upstream commit).
   - Accept only if the capped build, `ctest` (ALL_TESTS) and the branch's gate check pass. Otherwise abort the rebase and mark the branch `needs-rebase`.
4. **Regenerate** `dev-tideseed`: `git branch -f dev-tideseed upstream/latest`, then merge the accepted branches in queue order. Push with `--force-with-lease`.
5. **Build** main/dev/dev-tideseed under the memory rule (the `highs-build` skill, D-002), then run the smoke benchmark (the `highs-bench` skill, smoke mode).
6. **Report:** write `bench/results/sync-<date>.md`. Post to #agentlog only for a failure, unresolved conflict, regression, or a notable dev-vs-main shift.
