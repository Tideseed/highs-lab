---
name: highs-bench
description: Benchmark HiGHS arms (main, dev, dev-tideseed, lab branches, option variants) on MIPLIB with the lab harness and judge them with the gate. Use when asked to benchmark, measure, compare arms, check a speed-up, or decide whether a lab branch passes.
---
# Benchmark arms and apply the gate

1. **Define arms** in `bench/arms.toml`. Each needs a `binary`, plus optional `options = {...}` for HiGHS option variants. **Always include `dev`**; it is the control.
2. **Choose the mode:**
   - **Smoke:** 20 instances from `bench/sets/screen-v0.txt`, `--seeds 0 --time-limit 60`. It may run beside the LLM servers, and it only detects breakage or regressions.
   - **Clean (the gate):** the full screening set, `--seeds 0 1 2 --time-limit 300`, cores `5-9,15-19` (X925), **LLM servers stopped** in a declared window. Before the window, set `~/.config/cronrestore/hold-units` so experiment-guard does not restart them mid-run. Restart and verify the servers afterwards.
3. **Run it detached:**
   ```
   setsid nohup python3 bench/run.py --arms bench/arms.toml --only-arms dev <arm> \
     --set bench/sets/screen-v0.txt --seeds 0 1 2 --time-limit 300 --out bench/results/raw/<date>-<what> > log 2>&1 &
   ```
   The runner resumes: rerunning it skips finished jobs.
4. **Analyze:** `python3 bench/analyze.py bench/results/raw/<id> --control dev [--identical] --md bench/results/<id>.md`.
   - Use `--identical` when the branch claims a pure speed-up. Any node or LP-iteration difference on a both-solved run is then a bug.
   - **Gate:** ratio ≤ 0.97, CI upper bound < 1, zero wrong answers, solved count ≥ dev.
5. **Record:** write a `vault/30-results/` note with arms and SHAs (from the RESOURCES json), the numbers, CI, wrong answers and verdict. Update the candidate note's `status` and run `scripts/candidates-index.py`.
6. **Don't:**
   - compare against a number from an earlier session
   - run analysis with default thread counts while solver lanes run
   - use A725 cores for timed runs
