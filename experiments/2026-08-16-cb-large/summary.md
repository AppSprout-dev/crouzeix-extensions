# First-session numerical scout

Date: 2026-08-16
Estimator: Johnson supporting-line boundary of W(A) (720 angles, 4 edge samples).
All random ensembles use `numpy.random.default_rng(seed)` with the seed recorded.

## Sanity checks (nilpotent shifts)

For the n-dimensional nilpotent Jordan block, W(S_n) is the disk of
radius cos(π/(n+1)). In particular n=2 gives w=1/2, ||S||=1, ratio=2.


## Completely-bounded probe ratios (Johnson)

Count: 11.  min=0.6771  median=1.0655  max=2.0000
Records with ratio > 2 + 10^{-3}: 0

## CB probe detail

| family | n | k | poly | ratio | ||F(A)|| | max||F||_W |
|--------|---|---|------|-------|----------|-------------|
| nilpotent_shift | 2 | 8 | rand_k8_deg3 | 1.0752 | 8.3594 | 7.7747 |
| nilpotent_shift | 4 | 8 | rand_k8_deg3 | 1.1017 | 13.0098 | 11.8091 |
| nilpotent_shift | 6 | 8 | rand_k8_deg4 | 1.0776 | 14.7127 | 13.6535 |
| perturbed_nilpotent | 4 | 8 | rand_k8_deg3 | 1.0925 | 12.7216 | 11.6448 |
| perturbed_nilpotent | 6 | 8 | rand_k8_deg3 | 1.0334 | 14.0925 | 13.6366 |
| random_triangular | 6 | 8 | rand_k8_deg3 | 0.6771 | 274.5543 | 405.4874 |
| random_triangular | 8 | 8 | rand_k8_deg3 | 0.9618 | 737.0567 | 766.3657 |
| mild_nonnormal | 6 | 8 | rand_k8_deg3 | 1.0031 | 263.0622 | 262.2521 |
| nilpotent_shift | 3 | 12 | rand_k12_deg3 | 1.0655 | 14.2793 | 13.4019 |
| grcar | 6 | 8 | rand_k8_deg3 | 1.0268 | 150.6879 | 146.7553 |
| nilpotent_shift | 2 | 8 | z*I_8 | 2.0000 | 1.0000 | 0.5000 |

## Large cb probes (k ≥ 8, degree ≥ 3)

Count: 10.  max ratio = 1.1017.  All finite; none treated as a counter-example if they stay ≤ 2 + 1e-3.
Records with ratio ≥ 1.5 (approaching 2 from below): 0
- nilpotent_shift n=4 k=8 rand_k8_deg3 seed=8002  ratio=1.1017
- perturbed_nilpotent n=4 k=8 rand_k8_deg3 seed=8004  ratio=1.0925
- nilpotent_shift n=6 k=8 rand_k8_deg4 seed=8003  ratio=1.0776
- nilpotent_shift n=2 k=8 rand_k8_deg3 seed=8001  ratio=1.0752
- nilpotent_shift n=3 k=12 rand_k12_deg3 seed=8009  ratio=1.0655
- perturbed_nilpotent n=6 k=8 rand_k8_deg3 seed=8005  ratio=1.0334
- grcar n=6 k=8 rand_k8_deg3 seed=8010  ratio=1.0268
- mild_nonnormal n=6 k=8 rand_k8_deg3 seed=8008  ratio=1.0031
- random_triangular n=8 k=8 rand_k8_deg3 seed=8007  ratio=0.9618
- random_triangular n=6 k=8 rand_k8_deg3 seed=8006  ratio=0.6771

## Interpretation

- Scalar Johnson ratios are consistent with the settled theorem (universal 2).
- The 2×2 nilpotent shift attains 2 and is the first Lean special-class target.
- CB probes are *empirical* (finite k, Johnson sampling of ∂W).
- No cb probe in this run is a candidate counter-example to cb=2.

