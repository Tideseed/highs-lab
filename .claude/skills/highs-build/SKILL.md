---
name: highs-build
description: Build a HiGHS arm or lab branch safely on the shared DGX Spark (capped memory/CPU, memory gate, separate build dir) and run its unit tests. Use when asked to build HiGHS, compile a lab branch, rebuild dev/main/dev-tideseed, or run HiGHS ctest.
---
# Build a HiGHS arm or branch

1. **Worktree, not the main checkout:** `git -C ~/git_repositories/highs worktree add ../highs-wt/<name> <ref>`.
   Arms: `main` = `upstream/master`, `dev` = `upstream/latest`, `dev-tideseed`, and `lab/<idea>`.
2. **Memory gate:** `scripts/build-arm.sh` refuses below 30 GB `MemAvailable`. If it refuses:
   - Check whether the local agents are busy (`deep-status`, `agent-status`).
   - Idle: they may be stopped for the build and must be restarted and verified afterwards (D-002).
   - Busy: skip the build and notify #agentlog. Never lower the gate or raise the cap.
3. **Build:** `scripts/build-arm.sh <src> ~/git_repositories/highs-builds/<name> Release [-DBUILD_TESTING=OFF]`.
   - `Prof` gives RelWithDebInfo with frame pointers, for perf.
   - The compile runs in a systemd scope capped at `MemoryMax=12G`, `CPUQuota=600%`. `JOBS` defaults to 4.
   - Logs are `<builddir>.configure.log` and `<builddir>.build.log`.
4. **Unit tests** need `-DALL_TESTS=ON`; FAST_BUILD otherwise builds only 3 smoke tests. Use a separate `<name>-test` build dir so the benchmark binary is untouched. Run `ctest -j4 --timeout 900` pinned to the A725 cores (`taskset -c 10-14`) inside a capped scope.
5. Run long builds detached (`setsid nohup ... &`) and wait on the artifact or an `EXIT` line, never on a process name.

Never build CUDA/PDLP-GPU variants without the full host rule (nvcc is a JIT-class build: attended, one per window).
