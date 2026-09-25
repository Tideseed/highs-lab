#!/usr/bin/env bash
# Capped build of one HiGHS source tree.  build-arm.sh <src> <builddir> [Release|RelWithDebInfo|Prof] [extra cmake args...]
# Every compile on the Spark runs in a memory/CPU-capped systemd scope (see ~/CLAUDE.md, capped-build rule).
set -euo pipefail
SRC=$1; BLD=$2; TYPE=${3:-Release}; shift 3 || shift $#
EXTRA=()
if [ "$TYPE" = Prof ]; then TYPE=RelWithDebInfo; EXTRA+=(-DCMAKE_CXX_FLAGS=-fno-omit-frame-pointer -DCMAKE_C_FLAGS=-fno-omit-frame-pointer); fi
JOBS=${JOBS:-4}
AVAIL=$(awk '/MemAvailable/{print int($2/1048576)}' /proc/meminfo)
MIN=${MIN_AVAIL_GB:-30}
if [ "$AVAIL" -lt "$MIN" ]; then echo "REFUSE: MemAvailable ${AVAIL} GB < ${MIN} GB"; exit 3; fi
cmake -S "$SRC" -B "$BLD" -DCMAKE_BUILD_TYPE="$TYPE" "${EXTRA[@]}" "$@" > "$BLD.configure.log" 2>&1 || { mkdir -p "$BLD"; cmake -S "$SRC" -B "$BLD" -DCMAKE_BUILD_TYPE="$TYPE" "${EXTRA[@]}" "$@" > "$BLD.configure.log" 2>&1; }
systemd-run --user --scope --quiet -p MemoryMax=12G -p MemorySwapMax=0 -p CPUQuota=600% taskset -c "${BUILD_CORES:-0-4,10-14}" \
  cmake --build "$BLD" -j "$JOBS" > "$BLD.build.log" 2>&1
echo "BUILT $BLD $(git -C "$SRC" rev-parse --short HEAD)"
