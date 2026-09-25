---
name: highs-profile
description: Profile HiGHS with perf to find where time actually goes (by function and solver phase) and turn the result into candidate priorities. Use when asked to profile HiGHS, find hotspots, explain a slow instance, or decide which codebase-map candidate to implement next.
---
# Profile HiGHS

1. **Build the profiling binary:** `scripts/build-arm.sh <src> ~/git_repositories/highs-builds/<name>-prof Prof -DBUILD_TESTING=OFF`. That is RelWithDebInfo with `-fno-omit-frame-pointer`.
2. **perf access:** the host defaults to `kernel.perf_event_paranoid=4`, which blocks perf.
   - Lower it to 2 only for the profiling session: `sudo -n sysctl -w kernel.perf_event_paranoid=2`.
   - Restore 4 afterwards, and note both in the journal.
3. **Record,** pinned to an X925 core with a memory cap:
   ```
   systemd-run --user --scope -p MemoryMax=10G taskset -c 7 perf record -F 499 -g -o X.perf.data \
     <highs> --model_file <inst> --options_file opts   # opts: threads = 1, time_limit = 60
   ```
4. **Report:**
   - `perf report -i X.perf.data --no-children --sort symbol --stdio | head -60` gives the flat profile.
   - `--children` gives inclusive time per phase function: `HighsMipSolver::run`, `presolve`, `evaluateRootNode`, `HighsLpRelaxation::run`, `HighsSearch`, `HighsPrimalHeuristics::*`, `HighsDomain::propagate`, `HEkk*`, `HFactor*`.
   - Aggregate across about 15 screening instances plus a few large LPs; one instance is an anecdote.
5. **Update the candidate notes:** set `profiled_share:` to the inclusive share of the candidate's function(s), then run `scripts/candidates-index.py`. A code candidate needs a share of at least 1–2 % to be worth a branch.
6. HiGHS's own timing log is a cheap complement for the phase split (option `mip_...` profiling / `timeless_log=false`).
