# Tutorial 2 — Run a clean acceptance benchmark

A claim needs the full MIPLIB 2017 benchmark set (240 instances), 300 s, pinned X925 cores, both local LLM servers
stopped, paired arms interleaved per instance, a control arm (`dev` = upstream latest) in the same run.

1. Get Berk's OK for the window (it stops Agent Fast and Agent Think). Tell the other sessions (`ListAgents`,
   `SendMessage`); the halit runner pauses automatically for `night-bench` / `hlab-` units.
2. `scripts/night-bench.sh <run-id> 300 "<seeds>"` via a systemd unit (not from a Claude session, so a session restart
   cannot kill it). It: claims the `box-window` lease (aborts if held; no `--force`), pauses the canaries, stops both
   servers, asserts ≥ 80 GB free, runs `run.py` (optional ablation phase via `ABLATION_ARMS` / `ABLATION_SET`), stops and
   awaits every `hlab-*` solver scope, restores and health-checks both servers, resumes the jobs, releases the lease and
   posts a summary to #agentlog. Arms: `ARMS="dev dts-vN"` in the unit's environment.
3. Analyse: `bench/analyze.py <dir> --control dev [--identical]` (SGM, bootstrap CI, gate, known-optimum coverage) and
   `bench/hard.py <dir> --control dev` (PDGI, a log-sampled estimate). Check solutions with `bench/solcheck.py`.
4. Gate (D-004): SGM ≤ 0.97 with CI upper < 1, 0 wrong, 0 crashed, solved ≥ control on paired runs; identical search
   where claimed. One seed is not replication.
