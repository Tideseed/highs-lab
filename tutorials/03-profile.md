# Tutorial 3 — Find where the time goes

1. `scripts/build-arm.sh <src> ~/git_repositories/highs-builds/<name>-prof Prof -DBUILD_TESTING=OFF` (frame pointers).
2. perf is blocked by default (`kernel.perf_event_paranoid=4`): lower to 2 with sudo only for the session and restore 4
   afterwards; note both in the journal.
3. Sweep: `TL=60 bench/profile/sweep.sh <prof-binary> bench/sets/profile-hard.txt /tmp/prof 0,1,2,3` (A725 cores; never
   while timing runs are going — memory bandwidth is shared), then `bench/profile/aggregate.py /tmp/prof [--incl]`.
4. For one hot symbol, find its callers from `perf script` stacks (see the vault journal 2026-09-25 for the snippet)
   before designing a fix: the s100 overrun was clique partitioning, not the analytic-centre IPM a static read blamed.
