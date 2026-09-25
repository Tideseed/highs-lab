# Benchmark design

## Arms
`main` (upstream master), `dev` (upstream latest, **the control**), `dev-tideseed` (latest + accepted lab branches), plus
one arm per lab branch or option variant under test. Definitions in `bench/arms.toml`.

## Instance sets (`bench/sets/`)
- `screen-v0.txt`: 30 MIPLIB 2017 benchmark instances that HiGHS 1.15.1 solved in 8–300 s single-threaded in the optopt
  study (runs300, strategy H0). v1 will be re-selected from a full 240-instance pass of `dev`.
- `gap-v0.txt`: 42 instances unsolved at 300 s in the same data: for primal integral / final gap.
- `s100.txt`: the time-limit overrun reproduction (upstream #3314).
Instances: MIPLIB 2017 benchmark set, already local (`~/data/optopt/miplib/inst`, `solu.txt`).

## Execution
One run per core on the Cortex-X925 cores (5–9, 15–19), `threads=1`, 8 GiB hard cap per run (systemd scope, no swap),
seeds {0,1,2} for gated measurements, arms interleaved per instance+seed in shuffled order. A `RESOURCES-*.json`
beside each result directory records arms, binary hashes, load, free memory and whether the LLM servers were up.

## Metrics (`bench/analyze.py`)
- Shifted geometric mean of solve time (shift 10 s; unsolved at the limit), ratio vs `dev` with paired bootstrap
  95 % CI over instances; also on instances solved by both.
- Solved count; overrun past the time limit (mean, max).
- Wrong answers: bound pair excluding the known optimum, or "Optimal" off by more than 1e-4 relative.
- `--identical`: equal nodes, LP iterations and objective on runs both arms solved (pure speed-up claims).
- For gap-set runs: primal-dual integral (from the HiGHS report), final gap.

## Gate
Ratio ≤ 0.97 with CI upper bound < 1, zero wrong answers, solved count ≥ `dev`. Pure speed-ups also need `--identical`.

## Smoke vs clean
- Smoke (daily sync): ~20 instances × seed 0 × 60 s beside running LLM servers; catches regressions and breakage only.
- Clean (declared windows): LLM servers stopped, full gate; after each accepted branch and weekly.
