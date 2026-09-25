#!/usr/bin/env bash
# Overnight full benchmark: all MIPLIB 2017 benchmark instances, arms stable/dev/dts-v2/dts-v2-nodse (ARMS below),
# pinned to the X925 cores.
# Clean acceptance window (Berk, 2026-09-25): stops BOTH local LLM servers (Agent Think llama-qwen38, Agent Fast
# ornith-vllm) and pauses the jobs that would call them overnight (tr-power-forecast-think, the two ornith canaries).
# Everything it stops is restored and verified at the end, and the hold entries expire on their own.
#   night-bench.sh <run-id> [time-limit=300] [seeds="0"]
set -uo pipefail
RUN=$1; TL=${2:-300}; SEEDS=${3:-0}
LAB=~/git_repositories/highs-lab
OUT=$LAB/bench/results/raw/$RUN
LOG=$LAB/bench/results/raw/$RUN.night.log
ARMS="stable dev dts-v2 dts-v2-nodse"
JOBS="15e9efd9b30b f663edfdcbff 36f278b0ee63"   # tr-power-forecast-think, local-model-canary, canary-hello
[ "$(date +%H)" -lt 12 ] && DAY=today || DAY=tomorrow
UNTIL=$(date -d "$DAY 07:30" +%Y-%m-%dT07:30:00%:z)
mkdir -p "$(dirname "$LOG")"
exec >>"$LOG" 2>&1
# a persistent timer fires at boot if the box was down at the scheduled time: never start in the daytime
if [ "$(date +%-H)" -ge 6 ] && [ -z "${FORCE_NIGHT_BENCH:-}" ]; then
  echo "$(date -Is) not starting outside 00:00-05:59"; exit 0
fi
echo "== $(date -Is) night bench $RUN tl=$TL seeds=$SEEDS"

post() {
  local key; key=$(grep -oE 'Secret key:\s+\S+' ~/git_repositories/buzz/.keys/agent-watch.key | awk '{print $3}')
  BUZZ_RELAY_URL=https://spark-865d.tail7fc95f.ts.net:3443 BUZZ_PRIVATE_KEY=$key \
    ~/.local/bin/buzz messages send --channel e37b52b0-ef35-49f9-8cc6-d231551ad362 --content "$1" >/dev/null 2>&1 || true
}

restore() {
  systemctl --user start llama-qwen38 ornith-vllm
  for i in $(seq 1 80); do
    a=$(systemctl --user is-active llama-qwen38); b=$(systemctl --user is-active ornith-vllm)
    curl -sf -m 5 http://127.0.0.1:8092/health >/dev/null && curl -sf -m 5 http://127.0.0.1:8094/v1/models >/dev/null \
      && [ "$a" = active ] && [ "$b" = active ] && break
    sleep 15
  done
  for j in $JOBS; do hermes cron resume $j >/dev/null 2>&1; sed -i "/^$j .*highs-lab night/d" ~/.config/cronrestore/hold-jobs; done
  sed -i '/^llama-qwen38 .*$/d; /^ornith-vllm .*$/d' ~/.config/cronrestore/hold-units
  echo "restore: llama-qwen38 $(systemctl --user is-active llama-qwen38) (health $(curl -sf -m5 -o /dev/null -w %{http_code} http://127.0.0.1:8092/health)), ornith-vllm $(systemctl --user is-active ornith-vllm) (models $(curl -sf -m5 -o /dev/null -w %{http_code} http://127.0.0.1:8094/v1/models)); jobs resumed: $JOBS"
}
trap restore EXIT

# 1. hold + pause + stop (both local servers)
printf 'llama-qwen38 until %s\nornith-vllm until %s\n' "$UNTIL" "$UNTIL" >> ~/.config/cronrestore/hold-units
for j in $JOBS; do
  echo "$j  # highs-lab night bench $RUN, released by the script" >> ~/.config/cronrestore/hold-jobs
  hermes cron pause $j >/dev/null 2>&1
done
if [ "$(deep-status 2>/dev/null | grep -c IDLE)" = 0 ]; then
  echo "Agent Think busy at start; waiting up to 30 min"
  for i in $(seq 1 60); do deep-status 2>/dev/null | grep -q IDLE && break; sleep 30; done
fi
post "HiGHS night bench $RUN starting: Agent Fast and Agent Think servers stopped until ~06:30 (clean benchmark window, Berk OK). Canaries and tr-power-forecast-think paused for the window."
systemctl --user stop llama-qwen38 ornith-vllm
sleep 15
A=$(systemctl --user is-active llama-qwen38); B=$(systemctl --user is-active ornith-vllm)
MEM=$(awk '/MemAvailable/{print int($2/1048576)}' /proc/meminfo)
echo "stopped: llama-qwen38=$A ornith-vllm=$B; MemAvailable $MEM GB"
if [ "$A" = active ] || [ "$B" = active ] || [ "$MEM" -lt 80 ]; then
  echo "ABORT: window not clean (llama-qwen38=$A ornith-vllm=$B MemAvailable=${MEM}G)"
  post "HiGHS night bench $RUN ABORTED before running: window not clean (Think $A, Fast $B, ${MEM} GB free). Restoring."
  exit 2
fi

# 2. run
cd $LAB
ls ~/data/optopt/miplib/inst | sed 's/\.mps\.gz$//' | shuf --random-source=<(yes 20260925) > bench/sets/miplib-bench-all.txt
NI=$(wc -l < bench/sets/miplib-bench-all.txt); NA=$(echo $ARMS | wc -w); NS=$(echo $SEEDS | wc -w)
echo "budget: $NI instances x $NA arms x $NS seeds = $((NI*NA*NS)) jobs, <= ${TL}s each on 10 cores: worst case $((NI*NA*NS*${TL%.*}/10/3600)) h; window ends 06:30. timeout stops run.py only; HiGHS scopes already running finish on their own (<= ${TL}s). Arms are interleaved per instance, so a partial night stays paired."
# hard stop at 06:30 so that Agent Think is back well before the morning (the runner is resumable)
DEADLINE=$(( $(date -d '06:30' +%s) - $(date +%s) )); [ $DEADLINE -lt 0 ] && DEADLINE=$(( DEADLINE + 86400 ))
timeout $DEADLINE python3 bench/run.py --arms bench/arms.toml --only-arms $ARMS --set bench/sets/miplib-bench-all.txt \
  --seeds $SEEDS --time-limit "$TL" --cores 5-9,15-19 --mem-reserve-gb 20 --out "$OUT" > "$OUT.run.log" 2>&1
python3 bench/analyze.py "$OUT" --control dev --md bench/results/$RUN.md > /dev/null 2>&1
python3 bench/hard.py "$OUT" --control dev --md bench/results/$RUN-hard.md > /dev/null 2>&1

# 3. restore (trap) and report
restore; trap - EXIT
SUMMARY=$(grep -E "^\| ($(echo $ARMS | tr ' ' '|')) " bench/results/$RUN.md | cut -c1-160)
post "HiGHS night bench $RUN done (tl=${TL}s, seeds $SEEDS). vs dev:
$SUMMARY
Agents restored: Think $(systemctl --user is-active llama-qwen38), Fast $(systemctl --user is-active ornith-vllm)."
echo "== $(date -Is) done"
