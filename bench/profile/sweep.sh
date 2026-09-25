#!/usr/bin/env bash
# Profile a binary on a list of instances (30 s each, 1 thread), 4 in parallel on the given cores.
# sweep.sh <highs-binary> <set-file> <outdir> [cores]
BIN=$1; SET=$2; OUT=$3; CORES=${4:-0,1,2,3}
mkdir -p "$OUT"; printf 'threads = 1\ntime_limit = %s\n' "${TL:-30}" > "$OUT/opts"
IFS=, read -ra C <<< "$CORES"
i=0
for inst in $(grep -v '^#' "$SET"); do
  core=${C[$((i % ${#C[@]}))]}
  ( systemd-run --user --scope --quiet -p MemoryMax=8G taskset -c "$core" perf record -q -F 999 -g -o "$OUT/$inst.data" \
      "$BIN" --model_file ~/data/optopt/miplib/inst/$inst.mps.gz --options_file "$OUT/opts" > "$OUT/$inst.log" 2>&1
    perf report -i "$OUT/$inst.data" --no-children --sort symbol --stdio 2>/dev/null | grep -E '^ +[0-9]' > "$OUT/$inst.self.txt"
    perf report -i "$OUT/$inst.data" --children --sort symbol --stdio 2>/dev/null | grep -E '^ +[0-9]' > "$OUT/$inst.incl.txt"
    rm -f "$OUT/$inst.data" ) &
  i=$((i+1))
  if (( i % ${#C[@]} == 0 )); then wait; fi
done
wait
echo SWEEP-DONE > "$OUT/DONE"
