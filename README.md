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

Author: Berk Orbay. Work carried out with Claude Code (Anthropic) as research assistant.
License: MIT (same as HiGHS).
