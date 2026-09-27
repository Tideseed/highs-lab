# highs-lab

Research lab for speeding up the [HiGHS](https://github.com/ERGO-Code/HiGHS) optimization solver and improving its MIP
gap closure. Solver changes live on branches of the public fork [Tideseed/HiGHS](https://github.com/Tideseed/HiGHS);
this repo holds the benchmark harness, the sync automation, the research vault and agent skills.

**AI-assisted research, not a proposed upstream PR.** HiGHS does not accept AI-generated pull requests to its solvers
(see its CONTRIBUTING.md). Findings that hold up are reported to the HiGHS developers as issues with evidence; they
decide whether and how to implement them.

- Arms: `main` (upstream release branch), `dev` (upstream `latest`), `dev-tideseed` (`latest` + accepted lab branches)
- Harness: `bench/run.py` (pinned, memory-capped, resumable) and `bench/analyze.py` (shifted geometric mean, paired
  bootstrap CI, wrong-answer check against MIPLIB 2017 `solu.txt`, identical-search check)
- Start at `vault/00-index/Home.md`; agent rules in `AGENTS.md`.

## Results (frozen 2026-09-27; see `vault/30-results/Final report.md`)
- `dev-tideseed` v4 (five branches, no X1) vs upstream latest, MIPLIB 2017 benchmark set, 300 s, clean window, one
  seed: SGM **0.969 [0.939, 0.996]**, solved 101 vs 98, 0 wrong — passes the gate on that seed, **not replicated**.
  Pre-registered replication D-006 (seeds 2+3, fresh controls): v4 vs latest 0.974 [0.959, 0.988], base vs latest
  0.993 [0.988, 0.998] — v4 −2.59 % (1.22–4.08 %), base −0.69 %; neither passes the 3 % gate or the zero-failure
  rule (bohle 8 GiB cap kills). No detected reference errors; 2,495/2,497 saved incumbents pass a strict recheck.
- Primal side (Mittelmann's MIPFEAS primal integral on the same runs): v4 vs latest 0.960 [0.913, 1.010]; latest vs
  v1.15.1 14 % better. Latest finds no incumbent on 25/233 feasible instances in 300 s: the next target.
- Local wins: s100 time-limit fix, bohle presolve 349 → ~50 s (P1), toguru presolve −50 %, chromaticindex −47 % after presolve, neos-787933 unsolved →
  3–5 s (experimental presolve rule X1, with losses elsewhere).
- A HiGHS correctness bug (HighsHashTree::find_common) with a fix; 0 wrong answers in every run.
- Tutorials: `tutorials/` (screen, clean benchmark, profile, new branch).

Author: Berk Orbay. Work carried out with Claude Code (Anthropic) as research assistant.
License: MIT (same as HiGHS).
