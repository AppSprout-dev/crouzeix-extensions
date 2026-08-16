# First-session numerical scout

Date: 2026-08-16
Estimator: Johnson supporting-line boundary of W(A) (720 angles, 4 edge samples).
All random ensembles use `numpy.random.default_rng(seed)` with the seed recorded.

## Sanity checks (nilpotent shifts)

For the n-dimensional nilpotent Jordan block, W(S_n) is the disk of
radius cos(π/(n+1)). In particular n=2 gives w=1/2, ||S||=1, ratio=2.

- n= 2  ||S||=1.000000  w≈0.500000  ratio(z)≈2.000000  theory_w=0.500000
- n= 3  ||S||=1.000000  w≈0.707107  ratio(z)≈1.414214  theory_w=0.707107
- n= 4  ||S||=1.000000  w≈0.809017  ratio(z)≈1.236068  theory_w=0.809017
- n= 5  ||S||=1.000000  w≈0.866025  ratio(z)≈1.154701  theory_w=0.866025
- n= 6  ||S||=1.000000  w≈0.900969  ratio(z)≈1.109916  theory_w=0.900969
- n= 7  ||S||=1.000000  w≈0.923880  ratio(z)≈1.082392  theory_w=0.923880
- n= 8  ||S||=1.000000  w≈0.939693  ratio(z)≈1.064178  theory_w=0.939693
- n= 9  ||S||=1.000000  w≈0.951057  ratio(z)≈1.051462  theory_w=0.951057
- n=10  ||S||=1.000000  w≈0.959493  ratio(z)≈1.042217  theory_w=0.959493
- n=11  ||S||=1.000000  w≈0.965926  ratio(z)≈1.035276  theory_w=0.965926
- n=12  ||S||=1.000000  w≈0.970942  ratio(z)≈1.029928  theory_w=0.970942

## Legacy Monte-Carlo vs Johnson (original harness matrices)

The original `np.random.randn` sampler underestimates max |p| on W(A).
High-degree monomials amplify the bias (the n=8 ratio ~6.5 was an artifact).

| n | poly | MC ratio | Johnson ratio | MC max\|p\| | Johnson max\|p\| |
|---|------|----------|---------------|------------|------------------|
| 2 | z^1 | 1.1897 | 1.1892 | 2.5775e+00 | 2.5787e+00 |
| 3 | z^2 | 1.0273 | 0.9794 | 2.0531e+01 | 2.1536e+01 |
| 4 | z^3 | 1.3058 | 0.9704 | 6.1054e+01 | 8.2158e+01 |
| 8 | z^7 | 6.5155 | 0.4530 | 2.3282e+04 | 3.3485e+05 |

## Scalar ratios (Johnson)

Count: 242.  min=0.0000  median=1.0474  max=2.0000
Records with ratio > 2 + 10^{-3}: 0

## Completely-bounded probe ratios (Johnson)

Count: 17.  min=1.0003  median=1.0923  max=2.0000
Records with ratio > 2 + 10^{-3}: 0

## CB probe detail

| family | n | k | poly | ratio | ||F(A)|| | max||F||_W |
|--------|---|---|------|-------|----------|-------------|
| nilpotent_shift | 2 | 2 | rand_k2_deg1 | 1.1887 | 3.9525 | 3.3251 |
| nilpotent_shift | 2 | 2 | rand_k2_deg1 | 1.2665 | 3.4319 | 2.7098 |
| nilpotent_shift | 2 | 3 | rand_k3_deg1 | 1.1075 | 5.3514 | 4.8321 |
| nilpotent_shift | 2 | 4 | rand_k4_deg1 | 1.1004 | 5.9383 | 5.3967 |
| nilpotent_shift | 2 | 2 | z*I_2 | 2.0000 | 1.0000 | 0.5000 |
| nilpotent_shift | 2 | 3 | z*I_3 | 2.0000 | 1.0000 | 0.5000 |
| nilpotent_shift | 3 | 2 | rand_k2_deg2 | 1.2290 | 5.3901 | 4.3859 |
| nilpotent_shift | 5 | 2 | rand_k2_deg2 | 1.0702 | 4.9309 | 4.6075 |
| nilpotent_shift | 8 | 2 | rand_k2_deg2 | 1.0188 | 4.4717 | 4.3892 |
| random_triangular | 4 | 2 | rand_k2_deg2 | 1.0450 | 53.7416 | 51.4293 |
| random_triangular | 4 | 3 | rand_k3_deg1 | 1.0923 | 15.9913 | 14.6403 |
| random_triangular | 8 | 2 | rand_k2_deg2 | 1.0188 | 72.8357 | 71.4928 |
| random_triangular | 8 | 3 | rand_k3_deg1 | 1.2903 | 25.8686 | 20.0481 |
| mild_nonnormal | 4 | 2 | rand_k2_deg1 | 1.0061 | 5.3105 | 5.2782 |
| mild_nonnormal | 8 | 2 | rand_k2_deg1 | 1.0109 | 13.7143 | 13.5658 |
| cem_stiffness | 6 | 2 | rand_k2_deg1 | 1.0003 | 29.6199 | 29.6121 |
| cem_jacobian | 6 | 2 | rand_k2_deg1 | 1.0027 | 3.4855 | 3.4760 |

## Interpretation

- Scalar Johnson ratios are consistent with the settled theorem (universal 2).
- The 2×2 nilpotent shift attains 2 and is the first Lean special-class target.
- CB probes are *empirical* (finite k, low degree, Johnson sampling of ∂W).
- No cb probe in this run is a candidate counter-example to cb=2; larger
  amplifications and imported CEM snapshots are the next numerical step.

