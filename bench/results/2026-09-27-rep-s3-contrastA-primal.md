# MIPFEAS-style primal integral `/home/coulson/git_repositories/highs-lab/bench/results/raw/2026-09-27-rep-s3` (control `dev`)

699 runs on instances with a finite reference value; T = 300.0 s. Score per run: Mittelmann's primal integral P in [0, 2] (lower is better); table: shifted geometric mean (shift 0.001) over instances (seeds averaged first), ratio vs control with a paired instance bootstrap.

| arm | inst | SGM P | ratio vs ctl [95% CI] | mean P | incumbent by T | feasible at termination | SGM t first incumbent (s, found only) | within 1 % of z* by T | within 1e-4 by T |
|---|---|---|---|---|---|---|---|---|---|
| dev | 233 | 0.0688 | 1.000 [1.000, 1.000] | 0.3855 | 211/233 | 211/233 | 3.1 | 150/233 | 127/233 |
| dts-v2-nodse | 233 | 0.0664 | 0.966 [0.942, 0.985] | 0.3744 | 210/233 | 211/233 | 2.9 | 152/233 | 128/233 |
| dts-v4 | 233 | 0.0648 | 0.942 [0.896, 0.993] | 0.3620 | 210/233 | 210/233 | 2.8 | 151/233 | 124/233 |

## Runs with no incumbent by T

- **dev** (22): app1-2 s3, cryptanalysiskb128n5obj16 s3, fhnw-binpack4-48 s3, germanrr s3, gfd-schedulen180f7d50m30k18 s3, lectsched-5-obj s3, neos-1354092 s3, neos-2746589-doon s3, neos-3656078-kumeu s3, neos-5104907-jarama s3, ns1644855 s3, ns1760995 s3, ns1952667 s3, peg-solitaire-a3 s3, physiciansched3-3 s3, radiationm40-10-02 s3, rail01 s3, rail02 s3, square41 s3, square47 s3, supportcase19 s3, supportcase22 s3
- **dts-v2-nodse** (23): app1-2 s3, blp-ar98 s3, cryptanalysiskb128n5obj16 s3, fhnw-binpack4-48 s3, germanrr s3, gfd-schedulen180f7d50m30k18 s3, lectsched-5-obj s3, neos-1354092 s3, neos-2746589-doon s3, neos-3656078-kumeu s3, neos-5104907-jarama s3, ns1644855 s3, ns1760995 s3, ns1952667 s3, peg-solitaire-a3 s3, physiciansched3-3 s3, radiationm40-10-02 s3, rail01 s3, rail02 s3, square41 s3, square47 s3, supportcase19 s3, supportcase22 s3
- **dts-v4** (23): app1-2 s3, blp-ar98 s3, bnatt400 s3, cryptanalysiskb128n5obj16 s3, fhnw-binpack4-48 s3, germanrr s3, gfd-schedulen180f7d50m30k18 s3, neos-1354092 s3, neos-3024952-loue s3, neos-3656078-kumeu s3, neos-5104907-jarama s3, ns1644855 s3, ns1760995 s3, ns1952667 s3, peg-solitaire-a3 s3, physiciansched3-3 s3, radiationm40-10-02 s3, rail01 s3, rail02 s3, square41 s3, square47 s3, supportcase19 s3, supportcase22 s3

## Largest per-instance differences (|ΔP| ≥ 0.05, seed mean)

| arm | instance | P arm | P ctl | ΔP |
|---|---|---|---|---|
| dts-v2-nodse | s100 | 0.185 | 1.226 | -1.041 |
| dts-v2-nodse | rd-rplusc-21 | 1.397 | 1.977 | -0.580 |
| dts-v2-nodse | k1mushroom | 0.898 | 1.087 | -0.189 |
| dts-v2-nodse | s250r10 | 0.759 | 0.921 | -0.162 |
| dts-v2-nodse | bab6 | 1.061 | 1.221 | -0.161 |
| dts-v2-nodse | savsched1 | 0.874 | 0.978 | -0.103 |
| dts-v2-nodse | neos-4763324-toguru | 0.379 | 0.480 | -0.101 |
| dts-v2-nodse | neos-3024952-loue | 1.384 | 1.452 | -0.068 |
| dts-v2-nodse | neos-4532248-waihi | 0.423 | 0.487 | -0.064 |
| dts-v2-nodse | co-100 | 0.533 | 0.587 | -0.054 |
| dts-v2-nodse | opm2-z10-s4 | 0.380 | 0.432 | -0.052 |
| dts-v2-nodse | chromaticindex1024-7 | 0.179 | 0.109 | +0.070 |
| dts-v2-nodse | buildingenergy | 1.198 | 1.023 | +0.175 |
| dts-v4 | rd-rplusc-21 | 0.654 | 1.977 | -1.323 |
| dts-v4 | s100 | 0.169 | 1.226 | -1.056 |
| dts-v4 | momentum1 | 0.245 | 1.227 | -0.982 |
| dts-v4 | neos-2657525-crna | 0.190 | 0.801 | -0.612 |
| dts-v4 | lectsched-5-obj | 1.488 | 2.000 | -0.512 |
| dts-v4 | radiationm18-12-05 | 0.165 | 0.604 | -0.440 |
| dts-v4 | csched007 | 0.291 | 0.516 | -0.225 |
| dts-v4 | k1mushroom | 0.916 | 1.087 | -0.171 |
| dts-v4 | neos-2746589-doon | 1.837 | 2.000 | -0.163 |
| dts-v4 | neos-3004026-krka | 0.055 | 0.192 | -0.137 |
| dts-v4 | rocI-4-11 | 0.071 | 0.205 | -0.134 |
| dts-v4 | bab6 | 1.096 | 1.221 | -0.126 |
| dts-v4 | bab2 | 1.290 | 1.416 | -0.125 |
| dts-v4 | s250r10 | 0.813 | 0.921 | -0.107 |
| dts-v4 | neos-1456979 | 0.107 | 0.205 | -0.098 |
| dts-v4 | pk1 | 0.026 | 0.122 | -0.095 |
| dts-v4 | neos-4763324-toguru | 0.388 | 0.480 | -0.092 |
| dts-v4 | supportcase42 | 0.206 | 0.290 | -0.084 |
| dts-v4 | neos-4532248-waihi | 0.420 | 0.487 | -0.067 |
| dts-v4 | savsched1 | 0.913 | 0.978 | -0.064 |
| dts-v4 | ns1208400 | 0.208 | 0.268 | -0.060 |
| dts-v4 | comp07-2idx | 0.556 | 0.613 | -0.057 |
| dts-v4 | rocII-5-11 | 0.251 | 0.307 | -0.057 |
| dts-v4 | co-100 | 0.533 | 0.587 | -0.055 |
| dts-v4 | proteindesign121hz512p9 | 0.558 | 0.466 | +0.091 |
| dts-v4 | csched008 | 0.136 | 0.031 | +0.105 |
| dts-v4 | ns1830653 | 0.174 | 0.060 | +0.114 |
| dts-v4 | dws008-01 | 0.710 | 0.593 | +0.118 |
| dts-v4 | buildingenergy | 1.214 | 1.023 | +0.191 |
| dts-v4 | fastxgemm-n2r6s0t2 | 0.565 | 0.071 | +0.494 |
| dts-v4 | neos-3024952-loue | 2.000 | 1.452 | +0.548 |
