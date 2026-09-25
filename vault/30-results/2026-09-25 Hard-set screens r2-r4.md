# Hard-set screens r2–r4 (2026-09-25)

42 MIPLIB instances that HiGHS 1.15.1 left unsolved at 300 s (`bench/sets/gap-v0.txt`), seed 0, 60 s, 1 thread,
pinned to X925 cores. Screens, not measurements: one seed, and Agent Fast's server was loading during the start of r4
(memory-bandwidth heavy → random slowdowns of a few seconds early in r4, e.g. sorrell3 +4.5 s before the root LP in
one arm with an otherwise identical search path).

## r3 (dev vs lab-cpm, lab-ht, lab-sym, dev-tideseed = cpm+ht+sym+fw)
`bench/results/2026-09-25-hard-r3.md`. Only s100 moves outside noise (lab-cpm: 118 s overrun, no solution → 2.7 s,
feasible, gap 57 %). lab-ht, lab-sym: neutral on this set (lab-sym's gain is on chromaticindex, where the search
before the limit is dominated by presolve). No wrong answers, no crashes.

## r4 (dev vs lab-dse, dev-tideseed = previous + dse)
`bench/results/2026-09-25-hard-r4.md`.

| arm | solved | feasible | mean gap | worst overrun | wrong | crashed |
|---|---|---|---|---|---|---|
| dev | 0 | 33 | 54.4 % | 250.6 s | 0 | 0 |
| lab-dse | 1 | 34 | 51.7 % | 205.9 s | 0 | 0 |
| dev-tideseed | 1 | 35 | 50.6 % | 32.6 s | 0 | 0 |

- **neos-3004026-krka solved to optimality (opt 0) in ~20 s** with the DSE weight reuse; dev: 100 % gap at 60 s.
- Node ratios are not a speed proxy for lab-dse (weights change the pivoting, so the tree differs): per instance
  0.05–2.2×.
- Open: per-solve cost of caching weights at the end of every solve (O(num_col+num_row) copy); check on small
  instances and the night run.
