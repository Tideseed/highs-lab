# MIPFEAS-style primal integral `/home/coulson/git_repositories/highs-lab/bench/results/raw/2026-09-27-rep-s3` (control `dts-v2-nodse`)

699 runs on instances with a finite reference value; T = 300.0 s. Score per run: Mittelmann's primal integral P in [0, 2] (lower is better); table: shifted geometric mean (shift 0.001) over instances (seeds averaged first), ratio vs control with a paired instance bootstrap.

| arm | inst | SGM P | ratio vs ctl [95% CI] | mean P | incumbent by T | feasible at termination | SGM t first incumbent (s, found only) | within 1 % of z* by T | within 1e-4 by T |
|---|---|---|---|---|---|---|---|---|---|
| dev | 233 | 0.0688 | 1.035 [1.016, 1.061] | 0.3855 | 211/233 | 211/233 | 3.1 | 150/233 | 127/233 |
| dts-v2-nodse | 233 | 0.0664 | 1.000 [1.000, 1.000] | 0.3744 | 210/233 | 211/233 | 2.9 | 152/233 | 128/233 |
| dts-v4 | 233 | 0.0648 | 0.976 [0.932, 1.024] | 0.3620 | 210/233 | 210/233 | 2.8 | 151/233 | 124/233 |

## Runs with no incumbent by T

- **dev** (22): app1-2 s3, cryptanalysiskb128n5obj16 s3, fhnw-binpack4-48 s3, germanrr s3, gfd-schedulen180f7d50m30k18 s3, lectsched-5-obj s3, neos-1354092 s3, neos-2746589-doon s3, neos-3656078-kumeu s3, neos-5104907-jarama s3, ns1644855 s3, ns1760995 s3, ns1952667 s3, peg-solitaire-a3 s3, physiciansched3-3 s3, radiationm40-10-02 s3, rail01 s3, rail02 s3, square41 s3, square47 s3, supportcase19 s3, supportcase22 s3
- **dts-v2-nodse** (23): app1-2 s3, blp-ar98 s3, cryptanalysiskb128n5obj16 s3, fhnw-binpack4-48 s3, germanrr s3, gfd-schedulen180f7d50m30k18 s3, lectsched-5-obj s3, neos-1354092 s3, neos-2746589-doon s3, neos-3656078-kumeu s3, neos-5104907-jarama s3, ns1644855 s3, ns1760995 s3, ns1952667 s3, peg-solitaire-a3 s3, physiciansched3-3 s3, radiationm40-10-02 s3, rail01 s3, rail02 s3, square41 s3, square47 s3, supportcase19 s3, supportcase22 s3
- **dts-v4** (23): app1-2 s3, blp-ar98 s3, bnatt400 s3, cryptanalysiskb128n5obj16 s3, fhnw-binpack4-48 s3, germanrr s3, gfd-schedulen180f7d50m30k18 s3, neos-1354092 s3, neos-3024952-loue s3, neos-3656078-kumeu s3, neos-5104907-jarama s3, ns1644855 s3, ns1760995 s3, ns1952667 s3, peg-solitaire-a3 s3, physiciansched3-3 s3, radiationm40-10-02 s3, rail01 s3, rail02 s3, square41 s3, square47 s3, supportcase19 s3, supportcase22 s3

## Largest per-instance differences (|ΔP| ≥ 0.05, seed mean)

| arm | instance | P arm | P ctl | ΔP |
|---|---|---|---|---|
| dev | buildingenergy | 1.023 | 1.198 | -0.175 |
| dev | chromaticindex1024-7 | 0.109 | 0.179 | -0.070 |
| dev | opm2-z10-s4 | 0.432 | 0.380 | +0.052 |
| dev | co-100 | 0.587 | 0.533 | +0.054 |
| dev | neos-4532248-waihi | 0.487 | 0.423 | +0.064 |
| dev | neos-3024952-loue | 1.452 | 1.384 | +0.068 |
| dev | neos-4763324-toguru | 0.480 | 0.379 | +0.101 |
| dev | savsched1 | 0.978 | 0.874 | +0.103 |
| dev | bab6 | 1.221 | 1.061 | +0.161 |
| dev | s250r10 | 0.921 | 0.759 | +0.162 |
| dev | k1mushroom | 1.087 | 0.898 | +0.189 |
| dev | rd-rplusc-21 | 1.977 | 1.397 | +0.580 |
| dev | s100 | 1.226 | 0.185 | +1.041 |
| dts-v4 | momentum1 | 0.245 | 1.222 | -0.977 |
| dts-v4 | rd-rplusc-21 | 0.654 | 1.397 | -0.743 |
| dts-v4 | neos-2657525-crna | 0.190 | 0.801 | -0.612 |
| dts-v4 | lectsched-5-obj | 1.488 | 2.000 | -0.512 |
| dts-v4 | radiationm18-12-05 | 0.165 | 0.589 | -0.425 |
| dts-v4 | csched007 | 0.291 | 0.512 | -0.221 |
| dts-v4 | bab2 | 1.290 | 1.457 | -0.166 |
| dts-v4 | neos-2746589-doon | 1.837 | 2.000 | -0.163 |
| dts-v4 | rocI-4-11 | 0.071 | 0.204 | -0.133 |
| dts-v4 | neos-3004026-krka | 0.055 | 0.178 | -0.123 |
| dts-v4 | pk1 | 0.026 | 0.119 | -0.093 |
| dts-v4 | neos-1456979 | 0.107 | 0.197 | -0.090 |
| dts-v4 | supportcase42 | 0.206 | 0.285 | -0.079 |
| dts-v4 | chromaticindex1024-7 | 0.117 | 0.179 | -0.063 |
| dts-v4 | rocII-5-11 | 0.251 | 0.307 | -0.056 |
| dts-v4 | ns1208400 | 0.208 | 0.263 | -0.055 |
| dts-v4 | s250r10 | 0.813 | 0.759 | +0.054 |
| dts-v4 | csched008 | 0.136 | 0.031 | +0.105 |
| dts-v4 | ns1830653 | 0.174 | 0.061 | +0.113 |
| dts-v4 | dws008-01 | 0.710 | 0.586 | +0.124 |
| dts-v4 | fastxgemm-n2r6s0t2 | 0.565 | 0.071 | +0.494 |
| dts-v4 | neos-3024952-loue | 2.000 | 1.384 | +0.616 |
