# D-006 Pre-registered three-arm replication (2026-09-27, before any result)

Why: second Codex review on #5 (penultimate review + addendum). The v4 gate pass is one seed, and the proposed follow-up
(v4 alone against the historical clean1 dev control) broke AGENTS.md rule 2. Berk, 2026-09-27 ~09:15: "consider it,
update your plan and automatically go ahead if there is no blocking processes with higher priority". Written and
pushed BEFORE the first job starts; nothing below may be changed after results are seen (additions go in a dated
addendum that says so).

## Arms (pinned builds, all clean worktrees, binary newer than its source commit)
| arm | what | source | run.py binary_sha on clean2 |
|---|---|---|---|
| `dev` | upstream latest (fresh control) | 6293630a84 | 6dd634ca13f1 |
| `dts-v2-nodse` = **base** | clique marking + find_common fix, symmetry dense hash, free wins, P1 | 23395de1c6 | 1ba8373f0328 |
| `dts-v4` = **base + DSE cache** | base + lab/dse-cache (diff to base = exactly the dse-cache branch, 3 files) | cfa835da83 | c1ead1187f8f |
A job whose binary_sha differs from this table is excluded and reported.

## Design
- Set: all 240 MIPLIB 2017 benchmark instances (`bench/sets/miplib-bench-all.txt`), 300 s, 1 thread, default options,
  X925 cores 5–9 and 15–19, 8 GiB per run, `--mem-reserve-gb 20`, both local LLM servers stopped (clean window).
- Seeds: **2 and 3**, chosen now; seeds 0 and 1 have been looked at and are not reused. Seed 2 runs in a daytime window
  on 2026-09-27; seed 3 in the next window (night). Each window runs all three arms (fresh control inside the window);
  arm order shuffled per instance by run.py (balanced, `--shuffle-seed 12345`). New result directories
  `2026-09-27-rep-s2`, `…-rep-s3`.
- **Stopping rule: exactly these two seeds. No further seeds are added whatever the intervals show.** If a window is
  cut short, the paired runs completed are reported as such, with the missing count; no re-run to fill gaps except
  a harness crash (reported).

## Contrasts and decision rules (fixed now)
Primary contrasts: **A = base vs dev**, **B = base+DSE (v4) vs base**. Reported per seed AND pooled (instance
bootstrap over instances, both seeds of an instance kept together; seeds averaged per instance first, never treated
as independent instances).
Lead with: all-instance SGM ratio (shift 10 s) with 95 % CI, solved counts, wrong answers (solu.txt), crashes.
Diagnostics only: both-solved SGM, primal integral (bench/primal.py), PDGI, overruns, peak RSS, per-instance
regressions > 25 %.

- **Keep base (A)** if pooled ratio ≤ 0.97 with CI upper < 1, ratio < 1 on each seed separately, 0 wrong, 0 crashes
  (load timeouts excepted), solved ≥ dev pooled. If pooled ratio < 1 but not all of these: "no established aggregate
  effect"; base's local wins (s100, bohle, toguru, chromaticindex) stand on their own evidence either way.
- **Keep DSE cache (B)** only if pooled ratio < 1 with CI upper < 1 and 0 wrong / 0 crashes. Otherwise (CI crosses
  1, or worse): DSE is dropped from the combined branch — it changes the search, so the burden of proof is on it;
  "unestablished" means drop, and dev-tideseed becomes base.
- Contrast v4 vs dev is reported for continuity with clean2, not used for a decision.

## Not done
No option changes, no rebuilds, no instance selection. The feasibility checker is fixed (Codex review item 1) before
any solution from these runs is cited as feasible.

## Execution log (appended; the design above is unchanged)
- 2026-09-27 09:14:39 seed 2 started (unit `highs-rep-s2`, lease until 15:14). During the window the ops session's
  eptr2archive repair chain writes to ClickHouse (ceiling raised to 10.5 GB today); recorded as a contention factor
  (per-job loadavg is in every record), not a reason to change anything.
- Seed 3 scheduled for 2026-09-28 00:15 (transient timer `highs-rep-s3`, NOT reboot-safe); follow-up
  `scripts/d006-after.sh` computes contrasts A/B per seed and pooled, and after seed 2 the saved-solution recheck.

## Addendum 2026-09-27 10:1x (after Codex follow-up review; before any seed-2 result was looked at)
Clarifications only; the registered rules above are unchanged and will be reported as written.
- **Contention wording:** seed 2 is described as "both LLM servers stopped, **with recorded background contention**"
  (the ClickHouse repair chain). Fresh paired controls and shuffled order spread it across arms; load average alone
  cannot show it had no effect.
- **Contrast B and solved counts:** the registered B rule has no solved-count safeguard. The B result is reported as
  registered, and separately the general acceptance gate of AGENTS.md (ratio, CI, 0 wrong, 0 crashes, solved ≥ control)
  is checked before the combined branch is promoted; a favourable B interval does not waive a loss of solves.
- **Follow-up script bug (found by the reviewer):** `scripts/d006-after.sh` overwrote its positional arguments, so the
  recheck would have been skipped silently. Fixed (named flag, every step must succeed and write its output, the final
  log line is OK or FAILED with the failing steps); the running watcher was stopped and restarted on the fixed file
  (10:05); the analysis tools now exit non-zero on a missing control arm or empty input.
- 2026-09-27 14:06 seed 3 moved from the 00:15 timer to a daytime window on Berk's word ("if the machine is empty go for seed 3"); timer cancelled, unit `highs-rep-s3-day`, lease until 20:05. Same seed, arms, set and settings as registered.
