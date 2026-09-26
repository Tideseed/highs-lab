#!/usr/bin/env bash
# Profile-guided build of one HiGHS source tree, trained on non-MIPLIB families (disjoint from every benchmark set):
# 6 PGLib-UC + 3 ML4CO item placement + 3 ML4CO load balancing, 30 s each, sequential on one A725 core.
#   pgo-build.sh <src> <builddir>
set -e
S=$1; D=$2; B=$(dirname "$D")
F="-mcpu=native"
JOBS=${JOBS:-6} ~/git_repositories/highs-lab/scripts/build-arm.sh "$S" "$D" Release -DBUILD_TESTING=OFF \
  "-DCMAKE_CXX_FLAGS=$F -fprofile-generate -fprofile-update=single" "-DCMAKE_C_FLAGS=$F -fprofile-generate" \
  "-DCMAKE_SHARED_LINKER_FLAGS=-fprofile-generate" "-DCMAKE_EXE_LINKER_FLAGS=-fprofile-generate"
printf 'threads = 1\ntime_limit = 30\n' > "$D.train.opts"
TRAIN=$( (ls ~/data/optopt/pglib_uc/mps/*.mps.gz | shuf --random-source=<(yes 1) | head -6; \
          ls ~/data/optopt/ml4co/instances/1_item_placement/*/*.mps* 2>/dev/null | head -3; \
          ls ~/data/optopt/ml4co/instances/2_load_balancing/*/*.mps* 2>/dev/null | head -3) )
echo "$TRAIN" > "$D.train.list"
for f in $TRAIN; do systemd-run --user --scope --quiet -p MemoryMax=6G taskset -c 0 "$D/bin/highs" --model_file "$f" --options_file "$D.train.opts" > /dev/null 2>&1 || true; done
echo "gcda files: $(find "$D" -name '*.gcda' | wc -l)"
JOBS=${JOBS:-6} ~/git_repositories/highs-lab/scripts/build-arm.sh "$S" "$D" Release -DBUILD_TESTING=OFF \
  "-DCMAKE_CXX_FLAGS=$F -fprofile-use -fprofile-partial-training -Wno-missing-profile" "-DCMAKE_C_FLAGS=$F -fprofile-use -Wno-missing-profile" \
  "-DCMAKE_SHARED_LINKER_FLAGS=-fprofile-use" "-DCMAKE_EXE_LINKER_FLAGS=-fprofile-use"
echo PGO-DONE
