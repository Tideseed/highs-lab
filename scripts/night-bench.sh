#!/usr/bin/env bash
# Overnight full benchmark: all MIPLIB 2017 benchmark instances, arms main/dev/dev-tideseed, pinned to the X925 cores.
# Stops ONLY Agent Think's server (llama-qwen38) for the window and pauses its one night job; Agent Fast stays up.
# Everything it stops is restored and verified at the end, and the hold entries expire on their own.
#   night-bench.sh <run-id> [time-limit=300] [seeds="0"]
set -uo pipefail
RUN=$1; TL=${2:-300}; SEEDS=${3:-0}
LAB=~/git_repositories/highs-lab
OUT=$LAB/bench/results/raw/$RUN
LOG=$LAB/bench/results/raw/$RUN.night.log
THINK_JOB=15e9efd9b30b          # tr-power-forecast-think (hourly 00-05)
UNTIL=$(date -d 'tomorrow 07:30' +%Y-%m-%dT07:30:00%:z 2>/dev/null || date -d '07:30' +%Y-%m-%dT07:30:00%:z)
mkdir -p "$(dirname "$LOG")"
exec >>"$LOG" 2>&1
echo "== $(date -Is) night bench $RUN tl=$TL seeds=$SEEDS"

post() {
  local key; key=$(grep -oE 'Secret key:\s+\S+' ~/git_repositories/buzz/.keys/agent-watch.key | awk '{print $3}')
  BUZZ_RELAY_URL=https://spark-865d.tail7fc95f.ts.net:3443 BUZZ_PRIVATE_KEY=$key \
    ~/.local/bin/buzz messages send --channel e37b52b0-ef35-49f9-8cc6-d231551ad362 --content "$1" >/dev/null 2>&1 || true
}

restore() {
  systemctl --user start llama-qwen38
  for i in $(seq 1 60); do
    [ "$(systemctl --user is-active llama-qwen38)" = active ] && curl -sf -m 5 http://127.0.0.1:8092/health >/dev/null && break
    sleep 15
  done
  hermes cron resume $THINK_JOB >/dev/null 2>&1
  sed -i "/^$THINK_JOB .*highs-lab night/d" ~/.config/cronrestore/hold-jobs
  sed -i '/^llama-qwen38 .*$/d' ~/.config/cronrestore/hold-units
  echo "restore: llama-qwen38 $(systemctl --user is-active llama-qwen38), job $THINK_JOB resumed"
}
trap restore EXIT

# 1. hold + pause + stop (only Agent Think)
echo "llama-qwen38 until $UNTIL" >> ~/.config/cronrestore/hold-units
echo "$THINK_JOB  tr-power-forecast-think  # highs-lab night bench $RUN, released by the script" >> ~/.config/cronrestore/hold-jobs
hermes cron pause $THINK_JOB >/dev/null 2>&1
if [ "$(deep-status 2>/dev/null | grep -c IDLE)" = 0 ]; then
  echo "Agent Think busy at start; waiting up to 30 min"
  for i in $(seq 1 60); do deep-status 2>/dev/null | grep -q IDLE && break; sleep 30; done
fi
systemctl --user stop llama-qwen38
sleep 10

# 2. run
cd $LAB
ls ~/data/optopt/miplib/inst | sed 's/\.mps\.gz$//' | shuf --random-source=<(yes 20260925) > bench/sets/miplib-bench-all.txt
# hard stop at 06:30 so that Agent Think is back well before the morning (the runner is resumable)
DEADLINE=$(( $(date -d '06:30' +%s) - $(date +%s) )); [ $DEADLINE -lt 0 ] && DEADLINE=$(( DEADLINE + 86400 ))
timeout $DEADLINE python3 bench/run.py --arms bench/arms.toml --only-arms main dev dev-tideseed dev-tideseed-nodse --set bench/sets/miplib-bench-all.txt \
  --seeds $SEEDS --time-limit "$TL" --cores 5-9,15-19 --out "$OUT" > "$OUT.run.log" 2>&1
python3 bench/analyze.py "$OUT" --control dev --md bench/results/$RUN.md > /dev/null 2>&1
python3 bench/hard.py "$OUT" --control dev --md bench/results/$RUN-hard.md > /dev/null 2>&1

# 3. restore (trap) and report
restore; trap - EXIT
SUMMARY=$(grep -E '^\| (main|dev-tideseed) ' bench/results/$RUN.md | cut -c1-160)
post "HiGHS night bench $RUN done (tl=${TL}s, seeds $SEEDS). vs dev:
$SUMMARY
Agent Think restored: $(systemctl --user is-active llama-qwen38)."
echo "== $(date -Is) done"
