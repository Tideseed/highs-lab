#!/usr/bin/env bash
# D-006 follow-up for one seed window: wait for the night-bench "done" line, then the two pre-registered contrasts
# (A = base vs dev, B = v4 vs base) per seed, pooled when both seeds exist, and (optionally) the saved-solution recheck.
#   d006-after.sh <seed> [recheck]
set -uo pipefail
S=$1; LAB=~/git_repositories/highs-lab; R=$LAB/bench/results; RAW=$R/raw; RUN=2026-09-27-rep-s$S
PY=~/git_repositories/optopt/.venv/bin/python
until grep -q "^== .* done" $RAW/$RUN.night.log 2>/dev/null || grep -q "ABORT" $RAW/$RUN.night.log 2>/dev/null; do sleep 60; done
cd $LAB/bench
for c in "dev A" "dts-v2-nodse B"; do set -- $c
  python3 analyze.py $RAW/$RUN --control $1 --md $R/$RUN-contrast$2.md >/dev/null 2>&1
  python3 hard.py $RAW/$RUN --control $1 --md $R/$RUN-contrast$2-hard.md >/dev/null 2>&1
  python3 primal.py $RAW/$RUN --control $1 --md $R/$RUN-contrast$2-primal.md >/dev/null 2>&1
done
# pooled over seeds 2 and 3 (instances keep their seeds together; analyze.py averages seeds per instance first)
if [ -d $RAW/2026-09-27-rep-s2 ] && [ -d $RAW/2026-09-27-rep-s3 ] && grep -q "^== .* done" $RAW/2026-09-27-rep-s3.night.log 2>/dev/null; then
  P=$RAW/2026-09-27-rep-pooled; mkdir -p $P
  ln -sf $RAW/2026-09-27-rep-s2/*__s2.json $RAW/2026-09-27-rep-s3/*__s3.json $P/ 2>/dev/null
  for c in "dev A" "dts-v2-nodse B"; do set -- $c
    python3 analyze.py $P --control $1 --md $R/2026-09-27-rep-pooled-contrast$2.md >/dev/null 2>&1
    python3 primal.py $P --control $1 --md $R/2026-09-27-rep-pooled-contrast$2-primal.md >/dev/null 2>&1
  done
fi
if [ "${2:-}" = recheck ]; then
  for d in 2026-09-26-clean1 2026-09-27-clean2 $RUN; do
    systemd-run --user --scope -q -p MemoryMax=6G -p CPUQuota=100% --unit=hlab-recheck-$d-$$ \
      taskset -c 0-4 $PY recheck.py $RAW/$d --md $R/$d-recheck.md > $R/$d-recheck.log 2>&1
  done
fi
echo "$(date -Is) d006-after $S done" >> $RAW/$RUN.night.log
