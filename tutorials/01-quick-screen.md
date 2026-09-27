# Tutorial 1 — Screen a change quickly

Goal: find out fast whether a lab branch is worth a full measurement. Screens are not results.

1. Build the branch into its own directory (skill `highs-build`):
   `scripts/build-arm.sh ~/git_repositories/highs-wt/lab-<idea> ~/git_repositories/highs-builds/lab-<idea> Release -DBUILD_TESTING=OFF`
   The script refuses below 30 GB free and caps the compile (12 GB, 600 % CPU, A725 cores).
2. Add an arm to `bench/arms.toml`: `[lab-<idea>]` with `binary = ".../bin/highs"`.
3. Hardest instances first (Berk's rule): `bench/run.py --arms bench/arms.toml --only-arms dev lab-<idea> --set bench/sets/gap-v0.txt --seeds 0 --time-limit 60 --out bench/results/raw/<date>-<idea>-hard`
   then `cd bench && python3 hard.py results/raw/<date>-<idea>-hard --control dev` (PDGI, feasible, overrun).
4. Then small instances for no-regression: `bench/screen.py --arm lab-<idea> [--identical]` (fails fast on a wrong
   answer, crash, broken identical search, or ratio > 1.02).
5. Memory: run.py keeps `--mem-reserve-gb 20` free (memwatch sheds sessions at 12 GiB); with both LLM servers up it may
   run only 1–4 lanes. Never rebuild a build directory a running set uses.
