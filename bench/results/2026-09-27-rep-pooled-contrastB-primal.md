# MIPFEAS-style primal integral `/home/coulson/git_repositories/highs-lab/bench/results/raw/2026-09-27-rep-pooled` (control `dts-v2-nodse`)

1398 runs on instances with a finite reference value; T = 300.0 s. Score per run: Mittelmann's primal integral P in [0, 2] (lower is better); table: shifted geometric mean (shift 0.001) over instances (seeds averaged first), ratio vs control with a paired instance bootstrap.

| arm | inst | SGM P | ratio vs ctl [95% CI] | mean P | incumbent by T | feasible at termination | SGM t first incumbent (s, found only) | within 1 % of z* by T | within 1e-4 by T |
|---|---|---|---|---|---|---|---|---|---|
| dev | 233 | 0.0713 | 1.024 [1.009, 1.040] | 0.3873 | 419/466 | 419/466 | 3.1 | 301/466 | 250/466 |
| dts-v2-nodse | 233 | 0.0696 | 1.000 [1.000, 1.000] | 0.3825 | 418/466 | 419/466 | 2.9 | 303/466 | 253/466 |
| dts-v4 | 233 | 0.0687 | 0.988 [0.959, 1.017] | 0.3733 | 417/466 | 417/466 | 2.8 | 307/466 | 249/466 |

## Runs with no incumbent by T

- **dev** (47): app1-2 s2, app1-2 s3, bnatt400 s2, cryptanalysiskb128n5obj16 s2, cryptanalysiskb128n5obj16 s3, fhnw-binpack4-48 s2, fhnw-binpack4-48 s3, germanrr s2, germanrr s3, gfd-schedulen180f7d50m30k18 s2, gfd-schedulen180f7d50m30k18 s3, lectsched-5-obj s2, lectsched-5-obj s3, neos-1354092 s2, neos-1354092 s3, neos-2746589-doon s3, neos-3024952-loue s2, neos-3656078-kumeu s2, neos-3656078-kumeu s3, neos-4532248-waihi s2, neos-5104907-jarama s2, neos-5104907-jarama s3, ns1644855 s2, ns1644855 s3, ns1760995 s2, ns1760995 s3, ns1952667 s2, ns1952667 s3, peg-solitaire-a3 s2, peg-solitaire-a3 s3, physiciansched3-3 s3, radiationm40-10-02 s2, radiationm40-10-02 s3, rail01 s2, rail01 s3, rail02 s2, rail02 s3, s100 s2, square41 s2, square41 s3, square47 s2, square47 s3, supportcase19 s2, supportcase19 s3, supportcase22 s2, supportcase22 s3, triptim1 s2
- **dts-v2-nodse** (48): app1-2 s2, app1-2 s3, blp-ar98 s2, blp-ar98 s3, bnatt400 s2, cryptanalysiskb128n5obj16 s2, cryptanalysiskb128n5obj16 s3, fhnw-binpack4-48 s2, fhnw-binpack4-48 s3, germanrr s2, germanrr s3, gfd-schedulen180f7d50m30k18 s2, gfd-schedulen180f7d50m30k18 s3, lectsched-5-obj s2, lectsched-5-obj s3, neos-1354092 s2, neos-1354092 s3, neos-2746589-doon s3, neos-3024952-loue s2, neos-3656078-kumeu s2, neos-3656078-kumeu s3, neos-4532248-waihi s2, neos-5104907-jarama s2, neos-5104907-jarama s3, ns1644855 s2, ns1644855 s3, ns1760995 s2, ns1760995 s3, ns1952667 s2, ns1952667 s3, peg-solitaire-a3 s2, peg-solitaire-a3 s3, physiciansched3-3 s3, radiationm40-10-02 s2, radiationm40-10-02 s3, rail01 s2, rail01 s3, rail02 s2, rail02 s3, s100 s2, square41 s2, square41 s3, square47 s2, square47 s3, supportcase19 s2, supportcase19 s3, supportcase22 s2, supportcase22 s3
- **dts-v4** (49): app1-2 s2, app1-2 s3, blp-ar98 s2, blp-ar98 s3, bnatt400 s2, bnatt400 s3, cryptanalysiskb128n5obj16 s2, cryptanalysiskb128n5obj16 s3, fhnw-binpack4-48 s2, fhnw-binpack4-48 s3, germanrr s2, germanrr s3, gfd-schedulen180f7d50m30k18 s2, gfd-schedulen180f7d50m30k18 s3, lectsched-5-obj s2, neos-1354092 s2, neos-1354092 s3, neos-3024952-loue s2, neos-3024952-loue s3, neos-3656078-kumeu s2, neos-3656078-kumeu s3, neos-4532248-waihi s2, neos-5104907-jarama s2, neos-5104907-jarama s3, ns1644855 s2, ns1644855 s3, ns1760995 s2, ns1760995 s3, ns1952667 s2, ns1952667 s3, peg-solitaire-a3 s2, peg-solitaire-a3 s3, physiciansched3-3 s3, radiationm40-10-02 s2, radiationm40-10-02 s3, rail01 s2, rail01 s3, rail02 s2, rail02 s3, s100 s2, square41 s2, square41 s3, square47 s2, square47 s3, supportcase19 s2, supportcase19 s3, supportcase22 s2, supportcase22 s3, triptim1 s2

## Largest per-instance differences (|ΔP| ≥ 0.05, seed mean)

| arm | instance | P arm | P ctl | ΔP |
|---|---|---|---|---|
| dev | physiciansched3-3 | 1.369 | 1.922 | -0.552 |
| dev | blp-ar98 | 1.856 | 2.000 | -0.144 |
| dev | buildingenergy | 0.986 | 1.074 | -0.088 |
| dev | bab2 | 1.358 | 1.433 | -0.076 |
| dev | chromaticindex1024-7 | 0.106 | 0.167 | -0.061 |
| dev | savsched1 | 0.979 | 0.911 | +0.069 |
| dev | neos-4763324-toguru | 0.444 | 0.350 | +0.093 |
| dev | bab6 | 1.176 | 1.082 | +0.094 |
| dev | k1mushroom | 1.082 | 0.928 | +0.154 |
| dev | s250r10 | 0.780 | 0.626 | +0.154 |
| dev | s100 | 1.613 | 1.092 | +0.520 |
| dev | rd-rplusc-21 | 1.660 | 1.060 | +0.601 |
| dts-v4 | momentum1 | 0.200 | 1.207 | -1.007 |
| dts-v4 | rd-rplusc-21 | 0.623 | 1.060 | -0.437 |
| dts-v4 | neos-2657525-crna | 0.189 | 0.483 | -0.294 |
| dts-v4 | lectsched-5-obj | 1.744 | 2.000 | -0.256 |
| dts-v4 | radiationm18-12-05 | 0.208 | 0.435 | -0.227 |
| dts-v4 | csched007 | 0.239 | 0.399 | -0.160 |
| dts-v4 | bab2 | 1.295 | 1.433 | -0.138 |
| dts-v4 | comp07-2idx | 0.340 | 0.469 | -0.129 |
| dts-v4 | neos-2746589-doon | 1.787 | 1.888 | -0.101 |
| dts-v4 | rocI-4-11 | 0.144 | 0.213 | -0.069 |
| dts-v4 | buildingenergy | 1.009 | 1.074 | -0.066 |
| dts-v4 | supportcase42 | 0.171 | 0.223 | -0.052 |
| dts-v4 | neos-5107597-kakapo | 0.933 | 0.985 | -0.051 |
| dts-v4 | triptim1 | 1.163 | 1.111 | +0.052 |
| dts-v4 | eilA101-2 | 0.988 | 0.927 | +0.061 |
| dts-v4 | csched008 | 0.140 | 0.068 | +0.072 |
| dts-v4 | physiciansched3-3 | 2.000 | 1.922 | +0.078 |
| dts-v4 | fastxgemm-n2r6s0t2 | 0.295 | 0.048 | +0.247 |
| dts-v4 | neos-3024952-loue | 2.000 | 1.692 | +0.308 |
