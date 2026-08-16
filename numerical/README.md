# Numerical scouting

Scripts for computing empirical Crouzeix and completely-bounded ratios on:
- synthetic non-normal matrices,
- imported CEM operator snapshots (under `../data/imported/`).

## Quick start
```bash
pip install numpy scipy
python ratio_harness.py
```

Extend `ratio_harness.py` with amplification (matrix-valued polynomials) to probe the cb ratio.
