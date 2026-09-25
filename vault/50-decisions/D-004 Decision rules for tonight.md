# D-004: Decision rules, fixed before the night-1 result lands (2026-09-25 evening, review #4)

Gate set: the 240-instance night run (stable / dev / dts-v2 / dts-v2-nodse, 300 s, seed 0; more seeds on later
nights). The 33-instance small set cannot resolve a 3 % gate (CI half-width ≈ ±0.05) and censors ~18 % of runs at
120 s; it stays a screen.

1. **Code without DSE (dts-v2-nodse vs dev)** is accepted if: SGM ratio ≤ 0.97 with CI upper < 1, 0 wrong, 0
   crashed, solved ≥ dev on paired runs, and identical search on both-solved runs except instances where the
   find_common fix (C4) changes clique results (listed explicitly). Otherwise it stays `merged`.
2. **DSE (lab/dse-carry-weights) stays in dev-tideseed only if** ΔPDGI(dts-v2 − dts-v2-nodse) on the unsolved part of
   the night set has a CI excluding 0 in its favour **and** the SGM ratio dts-v2 / dts-v2-nodse is not worse (CI upper
   ≤ 1.00). If either fails: split into cache-only and carry-only arms (review #3) before any further claim.
3. **Robustness changes** (deadline checks, C1 as a time-limit fix) are judged on overrun (max and count > 5 s) and
   feasible-found count, not on speed.
4. A branch becomes `accepted` in queue.txt only with the gate artifact named next to it.

**Update 2026-09-25 21:50 (Berk):** Agent Fast is in use by another session tonight, so the clean 240-instance
acceptance run is **postponed** to a night when both local agents can stop (`scripts/night-bench.sh`, unchanged).
Tonight the timer runs `scripts/night-lite.sh` instead: no server stops, memory-budgeted lanes, paired runs only —
(A) hard set dev vs dts-v2 vs dts-v2-nodse (60 s, seed 0) for rule 2 evidence; (B) X1 on its 27 affected instances
(300 s, seeds 0–1). Rules 1–2 remain undecided until the clean run.
