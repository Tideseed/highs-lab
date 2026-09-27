# 2026-09-27 MIPFEAS-style primal integral (existing data, no new runs)

Berk asked whether we had checked Mittelmann's **MIPFEAS** benchmark (https://plato.asu.edu/ftp/mipfeas.html,
16 Sep 2026). We had not. It ranks solvers by how fast they find *good feasible solutions*.

## The benchmark
- 233 feasible MIPLIB 2017 instances, 600 s, 24 threads (Intel Core Ultra 9 285k; cuOpt also on a GB10).
- Per run: primal integral P = (1/T) ∫ p(t) dt, where p = 2 with no incumbent, 1 if z(t)·z* < 0, and otherwise
  |z(t) − z*| / max(|z(t)|, |z*|, 1).
- Ranking: shifted geometric mean of P (shift 0.001).
- Published (geometric mean, feasible found / 233, proven optimal):

| solver | SGM P | feasible | optimal |
|---|---|---|---|
| virtual best commercial (VMCS) | 0.0105 | 227 | 183 |
| ReXi | 0.0165 | 223 | 110 |
| SCIPConc 11.0 | 0.0274 | 216 | 106 |
| cuOpt 26.08 (B200 / GB10) | 0.0286 / 0.0393 | 226 | 78 / 73 |
| **HiGHS 1.15.1** | **0.0453** | **214** | **107** |
| SCIP 10.0.1 | 0.0755 | 204 | 77 |
| CBC 2.10.11 | 0.1015 | 188 | 78 |

HiGHS proves as many optima as the best open solvers but is weak on the **primal side**: 19 instances without any
feasible solution in 600 s.

## Same metric on our clean runs
`bench/primal.py` computes Mittelmann's P from the logged primal trajectory (final bound appended at the end time,
nothing credited beyond T), with z* from solu.txt (=opt= and =best=; 233 instances have one). **T = 300 s, 1 thread,
X925 core**, so absolute values are not comparable with the published table; only arms on the same runs are.
Hand-checked on one run (30n20b8 dev s1: 0.18837 both ways).

**clean1 (seed 0):**
| arm | inst | SGM P | ratio vs ctl [95% CI] | mean P | feasible runs | SGM t first incumbent (s, found only) | within 1 % of z* by T | within 1e-4 by T |
|---|---|---|---|---|---|---|---|---|
| dev | 233 | 0.0678 | 1.000 [1.000, 1.000] | 0.3994 | 207/233 | 2.8 | 152/233 | 121/233 |
| dts-v3 | 233 | 0.0650 | 0.959 [0.918, 1.001] | 0.3893 | 206/233 | 2.7 | 150/233 | 124/233 |
| dts-v3-pgo | 233 | 0.0645 | 0.952 [0.911, 0.994] | 0.3876 | 205/233 | 2.6 | 148/233 | 123/233 |
| stable | 233 | 0.0790 | 1.165 [1.076, 1.273] | 0.4110 | 208/233 | 2.8 | 150/233 | 118/233 |

**clean2 (seed 1):**
| arm | inst | SGM P | ratio vs ctl [95% CI] | mean P | feasible runs | SGM t first incumbent (s, found only) | within 1 % of z* by T | within 1e-4 by T |
|---|---|---|---|---|---|---|---|---|
| dev | 233 | 0.0682 | 1.000 [1.000, 1.000] | 0.4056 | 208/233 | 3.2 | 148/233 | 122/233 |
| dts-v4 | 233 | 0.0654 | 0.960 [0.913, 1.010] | 0.3901 | 208/233 | 2.9 | 155/233 | 129/233 |

Reading:
- latest vs release v1.15.1: stable 1.165 [1.076, 1.273], i.e. **latest is ~14 % better on the primal integral**,
  CI clear of 1. Upstream's own progress since the release is real on this axis too.
- Our branches: v3 0.959 [0.918, 1.001] (seed 0), PGO 0.952 [0.911, 0.994], v4 0.960 [0.913, 1.010] (seed 1).
  About 4 % better, consistent across both seeds, **CI touching or crossing 1**: suggestive, not established. The
  branches are speed fixes, so this is time-to-incumbent, not better heuristics: the no-incumbent count does not move.

## No incumbent by 300 s (seed 1)
- **dev** (25): app1-2 s1, bab6 s1, blp-ic98 s1, cryptanalysiskb128n5obj16 s1, fhnw-binpack4-48 s1, germanrr s1, gfd-schedulen180f7d50m30k18 s1, momentum1 s1, neos-1354092 s1, neos-3024952-loue s1, neos-3656078-kumeu s1, neos-5104907-jarama s1, ns1644855 s1, ns1760995 s1, ns1952667 s1, peg-solitaire-a3 s1, physiciansched3-3 s1, radiationm40-10-02 s1, rail01 s1, rail02 s1, s100 s1, square41 s1, square47 s1, supportcase19 s1, supportcase22 s1
- **dts-v4** (25): app1-2 s1, blp-ar98 s1, blp-ic98 s1, bnatt400 s1, cryptanalysiskb128n5obj16 s1, fhnw-binpack4-48 s1, germanrr s1, gfd-schedulen180f7d50m30k18 s1, lectsched-5-obj s1, momentum1 s1, neos-1354092 s1, neos-3656078-kumeu s1, neos-5104907-jarama s1, ns1644855 s1, ns1760995 s1, ns1952667 s1, peg-solitaire-a3 s1, radiationm40-10-02 s1, rail01 s1, rail02 s1, s100 s1, square41 s1, square47 s1, supportcase19 s1, supportcase22 s1

Both arms miss about 25 of 233. This is where HiGHS loses MIPFEAS, and nothing in the lab touched it: our two
SCIP-derived heuristics (one-opt, locks) improve an incumbent or needed one to exist. **Candidate next iteration
(after the freeze, Berk's call):** feasibility-first heuristics on this list (feasibility pump variants, fix-and-
propagate with restarts; rail01/02 are set-covering), scored by this metric at 600 s against latest.

Files: `bench/primal.py`, `bench/results/raw/2026-09-26-clean1.primal.md`, `bench/results/raw/2026-09-27-clean2.primal.md`.
