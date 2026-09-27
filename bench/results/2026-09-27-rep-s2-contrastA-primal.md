# MIPFEAS-style primal integral `/home/coulson/git_repositories/highs-lab/bench/results/raw/2026-09-27-rep-s2` (control `dev`)

699 runs on instances with a finite reference value; T = 300.0 s. Score per run: Mittelmann's primal integral P in [0, 2] (lower is better); table: shifted geometric mean (shift 0.001) over instances (seeds averaged first), ratio vs control with a paired instance bootstrap.

| arm | inst | SGM P | ratio vs ctl [95% CI] | mean P | incumbent by T | feasible at termination | SGM t first incumbent (s, found only) | within 1 % of z* by T | within 1e-4 by T |
|---|---|---|---|---|---|---|---|---|---|
| dev | 233 | 0.0682 | 1.000 [1.000, 1.000] | 0.3891 | 208/233 | 208/233 | 3.0 | 151/233 | 123/233 |
| dts-v2-nodse | 233 | 0.0670 | 0.983 [0.965, 1.000] | 0.3907 | 208/233 | 208/233 | 2.9 | 151/233 | 125/233 |
| dts-v4 | 233 | 0.0667 | 0.977 [0.943, 1.009] | 0.3845 | 207/233 | 207/233 | 2.9 | 156/233 | 125/233 |

## Runs with no incumbent by T

- **dev** (25): app1-2 s2, bnatt400 s2, cryptanalysiskb128n5obj16 s2, fhnw-binpack4-48 s2, germanrr s2, gfd-schedulen180f7d50m30k18 s2, lectsched-5-obj s2, neos-1354092 s2, neos-3024952-loue s2, neos-3656078-kumeu s2, neos-4532248-waihi s2, neos-5104907-jarama s2, ns1644855 s2, ns1760995 s2, ns1952667 s2, peg-solitaire-a3 s2, radiationm40-10-02 s2, rail01 s2, rail02 s2, s100 s2, square41 s2, square47 s2, supportcase19 s2, supportcase22 s2, triptim1 s2
- **dts-v2-nodse** (25): app1-2 s2, blp-ar98 s2, bnatt400 s2, cryptanalysiskb128n5obj16 s2, fhnw-binpack4-48 s2, germanrr s2, gfd-schedulen180f7d50m30k18 s2, lectsched-5-obj s2, neos-1354092 s2, neos-3024952-loue s2, neos-3656078-kumeu s2, neos-4532248-waihi s2, neos-5104907-jarama s2, ns1644855 s2, ns1760995 s2, ns1952667 s2, peg-solitaire-a3 s2, radiationm40-10-02 s2, rail01 s2, rail02 s2, s100 s2, square41 s2, square47 s2, supportcase19 s2, supportcase22 s2
- **dts-v4** (26): app1-2 s2, blp-ar98 s2, bnatt400 s2, cryptanalysiskb128n5obj16 s2, fhnw-binpack4-48 s2, germanrr s2, gfd-schedulen180f7d50m30k18 s2, lectsched-5-obj s2, neos-1354092 s2, neos-3024952-loue s2, neos-3656078-kumeu s2, neos-4532248-waihi s2, neos-5104907-jarama s2, ns1644855 s2, ns1760995 s2, ns1952667 s2, peg-solitaire-a3 s2, radiationm40-10-02 s2, rail01 s2, rail02 s2, s100 s2, square41 s2, square47 s2, supportcase19 s2, supportcase22 s2, triptim1 s2

## Largest per-instance differences (|ΔP| ≥ 0.05, seed mean)

| arm | instance | P arm | P ctl | ΔP |
|---|---|---|---|---|
| dts-v2-nodse | rd-rplusc-21 | 0.722 | 1.343 | -0.621 |
| dts-v2-nodse | s250r10 | 0.492 | 0.639 | -0.147 |
| dts-v2-nodse | k1mushroom | 0.957 | 1.076 | -0.119 |
| dts-v2-nodse | triptim1 | 1.897 | 2.000 | -0.103 |
| dts-v2-nodse | neos-4763324-toguru | 0.322 | 0.407 | -0.085 |
| dts-v2-nodse | chromaticindex1024-7 | 0.154 | 0.102 | +0.052 |
| dts-v2-nodse | splice1k1 | 0.521 | 0.434 | +0.087 |
| dts-v2-nodse | bab2 | 1.410 | 1.300 | +0.110 |
| dts-v2-nodse | blp-ar98 | 2.000 | 1.728 | +0.272 |
| dts-v2-nodse | physiciansched3-3 | 1.844 | 0.739 | +1.105 |
| dts-v4 | momentum1 | 0.155 | 1.189 | -1.034 |
| dts-v4 | rd-rplusc-21 | 0.591 | 1.343 | -0.752 |
| dts-v4 | comp07-2idx | 0.123 | 0.348 | -0.225 |
| dts-v4 | s250r10 | 0.480 | 0.639 | -0.159 |
| dts-v4 | buildingenergy | 0.803 | 0.949 | -0.146 |
| dts-v4 | satellites2-40 | 0.799 | 0.930 | -0.130 |
| dts-v4 | ns1830653 | 0.149 | 0.250 | -0.101 |
| dts-v4 | csched007 | 0.188 | 0.288 | -0.101 |
| dts-v4 | dws008-01 | 0.659 | 0.756 | -0.098 |
| dts-v4 | k1mushroom | 0.996 | 1.076 | -0.080 |
| dts-v4 | neos-5107597-kakapo | 0.924 | 1.002 | -0.078 |
| dts-v4 | mzzv11 | 0.343 | 0.418 | -0.075 |
| dts-v4 | neos-4763324-toguru | 0.340 | 0.407 | -0.067 |
| dts-v4 | proteindesign121hz512p9 | 0.401 | 0.342 | +0.059 |
| dts-v4 | splice1k1 | 0.509 | 0.434 | +0.075 |
| dts-v4 | 30n20b8 | 0.311 | 0.231 | +0.080 |
| dts-v4 | ns1208400 | 0.213 | 0.133 | +0.081 |
| dts-v4 | eilA101-2 | 0.980 | 0.862 | +0.119 |
| dts-v4 | neos-3004026-krka | 0.594 | 0.475 | +0.119 |
| dts-v4 | blp-ar98 | 2.000 | 1.728 | +0.272 |
| dts-v4 | physiciansched3-3 | 2.000 | 0.739 | +1.261 |
