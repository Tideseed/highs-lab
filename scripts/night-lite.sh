#!/usr/bin/env bash
# Night run WITHOUT stopping any server (Berk 2026-09-25: Agent Fast is in use by another session; the clean 240-instance
# acceptance run is postponed). Paired comparisons only (contention hits both arms alike); the memory budget in run.py
# sets the lanes (reserve 20 GB). Two run sets, then a summary to #agentlog.
#   A) hard set (42, 60 s, seed 0): dev vs dts-v2 vs dts-v2-nodse  -> DSE rule (D-004) evidence, v2 on the hard set
#   B) X1 changed-27 (300 s, seeds 0 1): dev vs lab-dsm            -> the X1 decision
set -uo pipefail
LAB=~/git_repositories/highs-lab; D=2026-09-26
LOG=$LAB/bench/results/raw/$D-night-lite.log
exec >>"$LOG" 2>&1
if [ "$(date +%-H)" -ge 6 ] && [ -z "${FORCE_NIGHT_BENCH:-}" ]; then echo "$(date -Is) not starting outside 00:00-05:59"; exit 0; fi
post() {
  local key; key=$(grep -oE 'Secret key:\s+\S+' ~/git_repositories/buzz/.keys/agent-watch.key | awk '{print $3}')
  BUZZ_RELAY_URL=https://spark-865d.tail7fc95f.ts.net:3443 BUZZ_PRIVATE_KEY=$key \
    ~/.local/bin/buzz messages send --channel e37b52b0-ef35-49f9-8cc6-d231551ad362 --content "$1" >/dev/null 2>&1 || true
}
release() {
  # Agent Think's night job was paused when Think was deactivated (21:3x); its hold line carries the "highs-lab night" marker
  hermes cron resume 15e9efd9b30b >/dev/null 2>&1
  sed -i "/^15e9efd9b30b .*highs-lab night/d" ~/.config/cronrestore/hold-jobs
}
trap release EXIT
cd $LAB
echo "== $(date -Is) night-lite start; MemAvailable $(awk '/MemAvailable/{print int($2/1048576)}' /proc/meminfo) GB; servers: fast=$(systemctl --user is-active ornith-vllm) think=$(systemctl --user is-active llama-qwen38)"
DEADLINE=$(( $(date -d '06:30' +%s) - $(date +%s) )); [ $DEADLINE -lt 0 ] && DEADLINE=$(( DEADLINE + 86400 ))
END=$(( $(date +%s) + DEADLINE ))
timeout $DEADLINE python3 bench/run.py --arms bench/arms.toml --only-arms dev dts-v2 dts-v2-nodse --set bench/sets/gap-v0.txt \
  --seeds 0 --time-limit 60 --cores 5-9,15-19 --mem-reserve-gb 20 --out bench/results/raw/$D-hard-v2 > bench/results/raw/$D-hard-v2.run.log 2>&1
(cd bench && python3 hard.py results/raw/$D-hard-v2 --control dev --md results/$D-hard-v2.md > /dev/null 2>&1)
LEFT=$(( END - $(date +%s) ))
if [ $LEFT -gt 600 ]; then
  timeout $LEFT python3 bench/run.py --arms bench/arms.toml --only-arms dev lab-dsm --set bench/sets/dsm-changed27.txt \
    --seeds 0 1 --time-limit 300 --cores 5-9,15-19 --mem-reserve-gb 20 --out bench/results/raw/$D-dsm-changed > bench/results/raw/$D-dsm-changed.run.log 2>&1
  python3 bench/analyze.py bench/results/raw/$D-dsm-changed --control dev --md bench/results/$D-dsm-changed.md > /dev/null 2>&1
  (cd bench && python3 hard.py results/raw/$D-dsm-changed --control dev --md results/$D-dsm-changed-hard.md > /dev/null 2>&1)
fi
A=$(grep -E '^\| dts-v2' bench/results/$D-hard-v2.md 2>/dev/null | cut -d'|' -f2-5 | tr '\n' ';')
B=$(grep -E '^\| lab-dsm' bench/results/$D-dsm-changed.md 2>/dev/null | cut -d'|' -f2-7 | tr '\n' ';')
post "HiGHS night-lite $D done (servers left running; paired runs only). Hard set PDGI vs dev: $A  X1 on its 27 instances vs dev: $B"
echo "== $(date -Is) done"
