# 2026-09-25 19:34 — memwatch HARD floor shed caused by a lab run set

**Timeline (CEST).** 19:19 Agent Think restarted after a capped one-opt build (both LLM servers resident, ~79 GB).
19:30 I launched the X1 comparison (27 instances, dev vs lab-dsm, 300 s, 10 lanes, 8 GB cap per run) with ~24 GB
free. 19:34:22 memwatch HARD floor (MemAvailable 9.4 GiB; the 10 HiGHS processes held ~16 GB RSS, top 3.8 GB) →
stopped the interactive tier (claude-desktop, claude-rc: Berk's sessions and this one), 19:35:54 stopped Agent Fast
(ornith-vllm). The run set died with the session (1/108 results; renamed INVALID-2026-09-25-dsm-changed).
21:3x Agent Fast restarted and verified; Agent Think deactivated on Berk's word (back with the night script at 06:30).

**Cause.** Per-run memory caps without a cap on the run set as a whole: 10 × 8 GB against ~24 GB free. Same class as
the 2026-09-23 shed (optopt D-003) — the rule "critical tier first" was known and I did not apply it to lanes.

**Fix.** `bench/run.py`: static lane budget = min(cores, (MemAvailable − reserve) / cap) and a per-launch admission
check (MemAvailable ≥ reserve + cap, serialised), `--mem-reserve-gb` default 20 (memwatch soft floor 12 GiB, hard 7);
peak RSS per run recorded. Night script passes the reserve explicitly. Dry-tested: 1 lane at reserve 50.
