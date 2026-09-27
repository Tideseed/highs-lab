# Housekeeping waiting for Berk's OK (2026-09-25 16:00)

A cleanup of one-off diagnostic builds and temporary profiling data was declined by the permission prompt, so nothing
was deleted. Candidates (no recorded result or tonight's arm points at them), ~2.7 GB:
- `~/git_repositories/highs-builds/`: cpm-shadow2, dts-pqc, lab-cpm-stat, lab-cpm-shadow, lab-cpm-prof, lab-cpm-test,
  t-cpm, t-fw, t-sym, t-dse, t-pcc (+ their .log/.out files), build-today.sh/.out
- `/tmp`: prof-dev, prof-hard, prof-dts, prof3, shadow, dse, pqc, bf, det, pcc, neos5.data, sor.data, misc logs
Kept on purpose: stable, main, dev, dev-test, dev-prof, dev-tideseed (v1), dev-tideseed-nodse (v1), dts-v2,
dts-v2-nodse, t-v2, lab-* release builds, dts-native, dts-pgo (+ PGO profiles), dts-prof. Disk is 31 % used.

## Done 2026-09-27 19:0x (Berk: "yes, do it now")
Deleted every item listed above that still existed (11 build dirs + logs, build-today.*, 12 /tmp scratch items):
2.9 GB freed. Nothing deleted outside this list. Remaining highs-builds: see `ls ~/git_repositories/highs-builds` — the
latest (dev), base (dts-v2-nodse), v4 (dts-v4) and stable builds are kept, as are the other arm/lab builds referenced
by recorded results (reproducible from their tags and branches; candidates for a later cleanup).
