# Numerical scouting

Scripts for computing empirical Crouzeix and completely-bounded ratios on:
- synthetic non-normal matrices,
- imported CEM operator snapshots (under `../data/imported/`).

## Quick start
```bash
pip install numpy scipy
python ratio_harness.py
python test_harness.py
```

`ratio_harness.py` writes CSV + a dated summary under `../experiments/YYYY-MM-DD-baseline/`
and regenerates `../data/synthetic/manifest.json`.

Useful flags:
- `--quick` — sanity, nilpotent family, and a small cb probe only
- `--large-cb` — only the large cb campaign (`k ≥ 8`, `degree ≥ 3`); seeded
- `--imported` — only static CEM snapshots under `../data/imported/`
- `--no-legacy-mc` — skip reproduction of the original Monte-Carlo sampler
- `--n-angles N` — Johnson supporting-line resolution (default 720)
- `--out DIR` — override the experiment directory

The default (non-`--quick`) run also includes the large cb campaign.

## What is computed
- **Scalar ratio** `||p(A)|| / max_{W(A)} |p|` for a polynomial `p`.
- **cb probe** `||F(A)|| / max_{W(A)} ||F(z)||` for a matrix-valued polynomial
  `F(z) = Σ C_j z^j`, with `F(A) = Σ C_j ⊗ A^j`.

`W(A)` is estimated by Johnson's supporting-line method (eigenvectors of
`Re(e^{-iθ} A)`). The original Monte-Carlo sampler underestimates
`max |p|` on `W(A)` and is kept only as `--legacy-mc` for comparison.

## Ensembles
See `ensembles.py`. Every random family takes an explicit seed. Structured
families (nilpotent / weighted / Grcar) are deterministic.
