# Tutorial 4 — Add a lab branch

1. `git -C ~/git_repositories/highs worktree add -b lab/<idea> ../highs-wt/lab-<idea> upstream/latest`
2. Keep the diff minimal and in HiGHS style; commit as Berk Orbay (noreply) with "AI-assisted (Claude Code)".
3. If it claims to be exact, prove it: a shadow build that computes old and new results on every call and aborts on a
   mismatch (example: `bench/patches/clique-marking-with-shadow-check.diff`) — it found two edge cases and a HiGHS bug.
4. Unit tests: a `-DALL_TESTS=ON` build, `ctest` (101 tests).
5. File a candidate note (`scripts/new-candidate.py`), add the branch to `bench/queue.txt` as `testing`, screen it
   (Tutorial 1), and only call it `accepted` with a named gate artifact (Tutorial 2).
6. Nothing goes to ERGO-Code/HiGHS without Berk's explicit per-item yes (their CONTRIBUTING refuses AI-generated
   solver PRs; findings go as issues with evidence).
