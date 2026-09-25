# highs-lab: rules for agents

This repo is the lab around **`Tideseed/HiGHS`**, a public fork of [ERGO-Code/HiGHS](https://github.com/ERGO-Code/HiGHS). The goal is to make HiGHS faster, or better at closing MIP gaps, on top of the newest upstream development branch. The work is AI-assisted research.

Read `vault/00-index/Home.md` first. It holds the current state, the three benchmark arms and the candidate list.

## Layout
| path | what |
|---|---|
| `../highs` | the fork checkout (remote `origin` = Tideseed/HiGHS, `upstream` = ERGO-Code/HiGHS) |
| `../highs-wt/<arm-or-branch>` | one git worktree per arm/branch |
| `../highs-builds/<name>` | one build directory per worktree; never build inside the source tree |
| `bench/` | harness (`run.py`, `analyze.py`), arm definitions, instance sets, results |
| `scripts/` | `build-arm.sh` (capped build), `highs-sync` (daily rebase, build and smoke test) |
| `vault/` | Obsidian vault: design, journal, results, codebase map, decisions, upstream drafts |
| `.claude/skills/` | procedures: build, bench, profile, new-idea, sync, upstream-issue |

## Branch model: a patch queue on top of upstream `latest`
- **Arms:**
  - `main` = upstream `master` (the last release)
  - `dev` = upstream `latest` (the control for every claim)
  - `dev-tideseed` = `dev` + the accepted `lab/*` branches, merged in `bench/queue.txt` order
- **Each idea is one `lab/<idea>` branch cut from `latest`**, with a README section in its first commit. It is rebased at every sync; the fork is ours, so `--force-with-lease` is fine there.
- **`dev-tideseed` is regenerated at every sync, never hand-edited.**
- Keep lab branches **minimal and single-purpose**. Their diff against `latest` is what an upstream issue links to.

## Hard rules
1. **No pull requests to ERGO-Code/HiGHS.** Its CONTRIBUTING.md does not accept AI-generated PRs to the solvers. Improvements go upstream as **issues** with measured evidence and a link to the fork branch. Every issue needs its own explicit approval from Berk Orbay before posting, and a prior-art search (`gh issue list -R ERGO-Code/HiGHS --state all --search ...`) first. See the `highs-upstream-issue` skill.
2. **Every claim is measured against `dev` in the same session.** A number from an earlier run is not a control.
3. **Gate:**
   - shifted geometric-mean time (shift 10 s) ratio ≤ 0.97, with the paired-bootstrap CI upper bound < 1
   - zero wrong answers against `solu.txt`
   - solved count not lower than `dev`

   Branches that claim a *pure speed-up* must also pass `--identical`: the same nodes, LP iterations and objective on every run that both arms solved.
4. **Every build is capped** (`scripts/build-arm.sh`: systemd scope `MemoryMax=12G`, `CPUQuota=600%`, and it refuses below 30 GB `MemAvailable`). Every solver run is capped (`bench/run.py`: 8 GiB, one pinned core).
5. **Commit identity:** Berk Orbay `5690139+berkorbay@users.noreply.github.com`. Credit the agent in message text, not in the author field.
6. **Avoid the areas the upstream developers are actively working on** unless the profile says the hot spot is there. That means MIP presolve and cliques (#3312, #3264, #3244), HiPO, and cut-correctness audits. Check `vault/10-design/Upstream activity.md`.
7. **Silent when clean.** Automation reports failures, unresolved conflicts and regressions only.

## Machine notes (DGX Spark, GB10)
- 10 × Cortex-X925 (cores 5–9, 15–19) and 10 × Cortex-A725 (cores 0–4, 10–14). **Benchmark only on the X925 cores**; an A725 is about 2× slower.
- The CPU and GPU share 121 GiB of memory with resident LLM servers. Clean measurements need those servers stopped, which happens only in declared windows (the host's own operator rules).
