# Invalid run: option sweep 2026-09-25 15:12–15:20

`bench/results/raw/INVALID-2026-09-25-opts-hard`: 26/42 runs per arm crashed/ended after ~23 s. The run used the
`dts-v2` build directory while I rebuilt it (query-count fix, ~15:16–15:20); processes launched during the rebuild
loaded a partially written libhighs. The old run.py hashed the binary once at start (executable only, not
libhighs), so nothing flagged it. Fixed in run.py (review #3 P0): hash = executable + libhighs, checked before every
job; a change aborts the run set. Rule: never rebuild a build directory that an active run set uses — build into a
new directory and switch arms.toml between run sets.
