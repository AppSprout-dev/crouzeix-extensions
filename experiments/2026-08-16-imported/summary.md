# First-session numerical scout

Date: 2026-08-16
Estimator: Johnson supporting-line boundary of W(A) (720 angles, 4 edge samples).
All random ensembles use `numpy.random.default_rng(seed)` with the seed recorded.

## Sanity checks (nilpotent shifts)

For the n-dimensional nilpotent Jordan block, W(S_n) is the disk of
radius cos(π/(n+1)). In particular n=2 gives w=1/2, ||S||=1, ratio=2.


## Scalar ratios (Johnson)

Count: 16.  min=1.0000  median=1.0000  max=1.0002
Records with ratio > 2 + 10^{-3}: 0

## Completely-bounded probe ratios (Johnson)

Count: 6.  min=1.0000  median=1.0000  max=1.0002
Records with ratio > 2 + 10^{-3}: 0

## CB probe detail

| family | n | k | poly | ratio | ||F(A)|| | max||F||_W |
|--------|---|---|------|-------|----------|-------------|
| imported_torquon | 8 | 2 | rand_k2_deg1 | 1.0000 | 5.5043 | 5.5043 |
| imported_torquon | 2 | 2 | rand_k2_deg1 | 1.0000 | 10230640.8083 | 10230640.8083 |
| imported_hygra | 3 | 2 | rand_k2_deg1 | 1.0000 | 281.8604 | 281.8604 |
| imported_hygra | 2 | 2 | rand_k2_deg1 | 1.0000 | 336.8450 | 336.8368 |
| imported_hygra | 2 | 2 | rand_k2_deg1 | 1.0002 | 119.0406 | 119.0172 |
| imported_hygra | 2 | 2 | rand_k2_deg1 | 1.0000 | 336.8335 | 336.8310 |

## Interpretation

- Scalar Johnson ratios are consistent with the settled theorem (universal 2).
- The 2×2 nilpotent shift attains 2 and is the first Lean special-class target.
- CB probes are *empirical* (finite k, Johnson sampling of ∂W).
- No cb probe in this run is a candidate counter-example to cb=2.

