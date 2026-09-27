#!/usr/bin/env bash
# D-006 follow-up for one seed window: wait for the night-bench "done" line, then the two pre-registered contrasts
# (A = base vs dev, B = v4 vs base) per seed, pooled when both seeds exist, and (optionally) the saved-solution recheck.
#   d006-after.sh <seed> [recheck]
# Every step must succeed AND write its output file; the final line is "d006-after <seed> OK" or "... FAILED: <steps>".
set -uo pipefail
SEED=$1; DO_RECHECK=${2:-}          # named: never read positional args after this line
LAB=~/git_repositories/highs-lab; R=$LAB/bench/results; RAW=$R/raw; RUN=2026-09-27-rep-s$SEED
PY=~/git_repositories/optopt/.venv/bin/python
LOG=$RAW/$RUN.night.log
FAILED=()
step() {  # step <name> <expected output file> <command...>
  local name=$1 out=$2; shift 2
  if "$@" && [ -s "$out" ]; then echo "$(date -Is) ok   $name"; else echo "$(date -Is) FAIL $name (rc=$?, out $out)"; FAILED+=("$name"); fi
}
until grep -q "^== .* done" "$LOG" 2>/dev/null || grep -q "ABORT" "$LOG" 2>/dev/null; do sleep 60; done
if grep -q "ABORT" "$LOG"; then echo "$(date -Is) d006-after $SEED FAILED: window aborted" >> "$LOG"; exit 1; fi
cd $LAB/bench
for pair in "dev:A" "dts-v2-nodse:B"; do
  ctl=${pair%%:*}; tag=${pair##*:}
  step "analyze $tag" $R/$RUN-contrast$tag.md python3 analyze.py $RAW/$RUN --control $ctl --md $R/$RUN-contrast$tag.md
  step "hard $tag" $R/$RUN-contrast$tag-hard.md python3 hard.py $RAW/$RUN --control $ctl --md $R/$RUN-contrast$tag-hard.md
  step "primal $tag" $R/$RUN-contrast$tag-primal.md python3 primal.py $RAW/$RUN --control $ctl --md $R/$RUN-contrast$tag-primal.md
done
if [ -d $RAW/2026-09-27-rep-s2 ] && [ -d $RAW/2026-09-27-rep-s3 ] && grep -q "^== .* done" $RAW/2026-09-27-rep-s3.night.log 2>/dev/null; then
  P=$RAW/2026-09-27-rep-pooled; mkdir -p $P
  ln -sf $RAW/2026-09-27-rep-s2/*__s2.json $RAW/2026-09-27-rep-s3/*__s3.json $P/
  for pair in "dev:A" "dts-v2-nodse:B"; do
    ctl=${pair%%:*}; tag=${pair##*:}
    step "pooled analyze $tag" $R/2026-09-27-rep-pooled-contrast$tag.md python3 analyze.py $P --control $ctl --md $R/2026-09-27-rep-pooled-contrast$tag.md
    step "pooled primal $tag" $R/2026-09-27-rep-pooled-contrast$tag-primal.md python3 primal.py $P --control $ctl --md $R/2026-09-27-rep-pooled-contrast$tag-primal.md
  done
fi
if [ "$DO_RECHECK" = recheck ]; then
  for d in 2026-09-26-clean1 2026-09-27-clean2 $RUN; do
    step "recheck $d" $R/$d-recheck.md systemd-run --user --scope -q -p MemoryMax=6G -p CPUQuota=100% --unit=hlab-recheck-$d-$$ \
      taskset -c 0-4 $PY recheck.py $RAW/$d --md $R/$d-recheck.md
  done
fi
if [ ${#FAILED[@]} -eq 0 ]; then echo "$(date -Is) d006-after $SEED OK" >> "$LOG"
else echo "$(date -Is) d006-after $SEED FAILED: ${FAILED[*]}" >> "$LOG"; exit 1; fi
