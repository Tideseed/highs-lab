# Housekeeping waiting for Berk's OK (2026-09-25 16:00)

A cleanup of one-off diagnostic builds and temporary profiling data was declined by the permission prompt, so nothing
was deleted. Candidates (no recorded result or tonight's arm points at them), ~2.7 GB:
- `~/git_repositories/highs-builds/`: cpm-shadow2, dts-pqc, lab-cpm-stat, lab-cpm-shadow, lab-cpm-prof, lab-cpm-test,
  t-cpm, t-fw, t-sym, t-dse, t-pcc (+ their .log/.out files), build-today.sh/.out
- `/tmp`: prof-dev, prof-hard, prof-dts, prof3, shadow, dse, pqc, bf, det, pcc, neos5.data, sor.data, misc logs
Kept on purpose: stable, main, dev, dev-test, dev-prof, dev-tideseed (v1), dev-tideseed-nodse (v1), dts-v2,
dts-v2-nodse, t-v2, lab-* release builds, dts-native, dts-pgo (+ PGO profiles), dts-prof. Disk is 31 % used.
