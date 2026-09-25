---
name: highs-new-idea
description: Start a new HiGHS improvement as a lab branch on top of upstream latest, with its intent recorded for the sync/auto-resolution and its vault note. Use when starting work on a codebase-map candidate or any new HiGHS change.
---
# Start a lab branch

1. `git -C ~/git_repositories/highs fetch upstream latest`, then create the worktree:
   `git -C ~/git_repositories/highs worktree add -b lab/<idea> ../highs-wt/lab-<idea> upstream/latest`.
2. **Intent comes first.** Append a line to `bench/queue.txt`: `lab/<idea> | <candidate ids> | <gate: identical|full> | <one-line intent>`. The auto-resolver reads this intent when upstream changes the same lines, so write it as the behaviour you want to preserve, not the diff.
3. **Keep the change minimal and single-purpose,** in HiGHS's own style (`.clang-format`, the naming of the surrounding code). No reformatting and no unrelated cleanups; the diff against `latest` is what upstream reads.
4. **Build and test:** the `highs-build` skill; `ctest` with ALL_TESTS must pass.
5. **Measure:** the `highs-bench` skill against `dev`. Use `--identical` for pure speed-ups.
6. **Record:** set the candidate note's status to `branch`, then `gated`, then accepted or rejected, with a log line each time. Put the results note in `vault/30-results/`. Commit as Berk Orbay (noreply).
7. **If accepted,** mark it `accepted` in `bench/queue.txt`; the next sync merges it into `dev-tideseed`. Push with `git push -u origin lab/<idea>`, using `--force-with-lease` after rebases.
