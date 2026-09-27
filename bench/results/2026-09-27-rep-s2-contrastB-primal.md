# MIPFEAS-style primal integral `/home/coulson/git_repositories/highs-lab/bench/results/raw/2026-09-27-rep-s2` (control `dts-v2-nodse`)

699 runs on instances with a finite reference value; T = 300.0 s. Score per run: Mittelmann's primal integral P in [0, 2] (lower is better); table: shifted geometric mean (shift 0.001) over instances (seeds averaged first), ratio vs control with a paired instance bootstrap.

| arm | inst | SGM P | ratio vs ctl [95% CI] | mean P | incumbent by T | feasible at termination | SGM t first incumbent (s, found only) | within 1 % of z* by T | within 1e-4 by T |
|---|---|---|---|---|---|---|---|---|---|
| dev | 233 | 0.0682 | 1.018 [1.000, 1.037] | 0.3891 | 208/233 | 208/233 | 3.0 | 151/233 | 123/233 |
| dts-v2-nodse | 233 | 0.0670 | 1.000 [1.000, 1.000] | 0.3907 | 208/233 | 208/233 | 2.9 | 151/233 | 125/233 |
| dts-v4 | 233 | 0.0667 | 0.994 [0.963, 1.021] | 0.3845 | 207/233 | 207/233 | 2.9 | 156/233 | 125/233 |

## Runs with no incumbent by T

- **dev** (25): app1-2 s2, bnatt400 s2, cryptanalysiskb128n5obj16 s2, fhnw-binpack4-48 s2, germanrr s2, gfd-schedulen180f7d50m30k18 s2, lectsched-5-obj s2, neos-1354092 s2, neos-3024952-loue s2, neos-3656078-kumeu s2, neos-4532248-waihi s2, neos-5104907-jarama s2, ns1644855 s2, ns1760995 s2, ns1952667 s2, peg-solitaire-a3 s2, radiationm40-10-02 s2, rail01 s2, rail02 s2, s100 s2, square41 s2, square47 s2, supportcase19 s2, supportcase22 s2, triptim1 s2
- **dts-v2-nodse** (25): app1-2 s2, blp-ar98 s2, bnatt400 s2, cryptanalysiskb128n5obj16 s2, fhnw-binpack4-48 s2, germanrr s2, gfd-schedulen180f7d50m30k18 s2, lectsched-5-obj s2, neos-1354092 s2, neos-3024952-loue s2, neos-3656078-kumeu s2, neos-4532248-waihi s2, neos-5104907-jarama s2, ns1644855 s2, ns1760995 s2, ns1952667 s2, peg-solitaire-a3 s2, radiationm40-10-02 s2, rail01 s2, rail02 s2, s100 s2, square41 s2, square47 s2, supportcase19 s2, supportcase22 s2
- **dts-v4** (26): app1-2 s2, blp-ar98 s2, bnatt400 s2, cryptanalysiskb128n5obj16 s2, fhnw-binpack4-48 s2, germanrr s2, gfd-schedulen180f7d50m30k18 s2, lectsched-5-obj s2, neos-1354092 s2, neos-3024952-loue s2, neos-3656078-kumeu s2, neos-4532248-waihi s2, neos-5104907-jarama s2, ns1644855 s2, ns1760995 s2, ns1952667 s2, peg-solitaire-a3 s2, radiationm40-10-02 s2, rail01 s2, rail02 s2, s100 s2, square41 s2, square47 s2, supportcase19 s2, supportcase22 s2, triptim1 s2

## Largest per-instance differences (|ΔP| ≥ 0.05, seed mean)

| arm | instance | P arm | P ctl | ΔP |
|---|---|---|---|---|
| dev | physiciansched3-3 | 0.739 | 1.844 | -1.105 |
| dev | blp-ar98 | 1.728 | 2.000 | -0.272 |
| dev | bab2 | 1.300 | 1.410 | -0.110 |
| dev | splice1k1 | 0.434 | 0.521 | -0.087 |
| dev | chromaticindex1024-7 | 0.102 | 0.154 | -0.052 |
| dev | neos-4763324-toguru | 0.407 | 0.322 | +0.085 |
| dev | triptim1 | 2.000 | 1.897 | +0.103 |
| dev | k1mushroom | 1.076 | 0.957 | +0.119 |
| dev | s250r10 | 0.639 | 0.492 | +0.147 |
| dev | rd-rplusc-21 | 1.343 | 0.722 | +0.621 |
| dts-v4 | momentum1 | 0.155 | 1.191 | -1.037 |
| dts-v4 | comp07-2idx | 0.123 | 0.342 | -0.218 |
| dts-v4 | buildingenergy | 0.803 | 0.951 | -0.147 |
| dts-v4 | rd-rplusc-21 | 0.591 | 0.722 | -0.131 |
| dts-v4 | satellites2-40 | 0.799 | 0.919 | -0.119 |
| dts-v4 | bab2 | 1.300 | 1.410 | -0.110 |
| dts-v4 | csched007 | 0.188 | 0.287 | -0.099 |
| dts-v4 | ns1830653 | 0.149 | 0.247 | -0.098 |
| dts-v4 | dws008-01 | 0.659 | 0.748 | -0.089 |
| dts-v4 | mzzv11 | 0.343 | 0.426 | -0.083 |
| dts-v4 | neos-5107597-kakapo | 0.924 | 0.999 | -0.075 |
| dts-v4 | map16715-04 | 0.328 | 0.384 | -0.056 |
| dts-v4 | 30n20b8 | 0.311 | 0.233 | +0.078 |
| dts-v4 | ns1208400 | 0.213 | 0.131 | +0.083 |
| dts-v4 | triptim1 | 2.000 | 1.897 | +0.103 |
| dts-v4 | eilA101-2 | 0.980 | 0.860 | +0.121 |
| dts-v4 | neos-3004026-krka | 0.594 | 0.439 | +0.155 |
| dts-v4 | physiciansched3-3 | 2.000 | 1.844 | +0.156 |
