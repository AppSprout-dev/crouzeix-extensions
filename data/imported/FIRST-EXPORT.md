# First data export (decision)

**Date:** 2026-08-16

## Decision
The first concrete data import will be a small set of **synthetic but CEM-motivated matrices** plus, when available, a handful of real (or anonymized) operators from:

1. Torquon-GB — stage stiffness / transfer matrices under mild non-normality (tolerances or asymmetric loading).
2. Hygra — multi-zone environmental or resource Jacobians (nearly-commuting families preferred for early joint tests).

## Immediate action
- Generate synthetic nilpotent-shift and random-triangular ensembles in `data/synthetic/` (already supported by the numerical harness). **Done, 2026-08-16:** see `data/synthetic/manifest.json`.
- Request or produce 3–5 small matrices from Torquon-GB test benches (dimension ≤ 32 preferred) and place them under `data/imported/torquon-gb/` with a short README (origin, date, any anonymization). **Done, 2026-08-16:** four stiffness operators from Torquon-GB@`2be4790` (Q4 element, MBB 2×2, end-plate 3×2, VDI flange). See `torquon-gb/README.md`.
- Same for Hygra under `data/imported/hygra/` when convenient. **Done, 2026-08-16:** four Jacobians from Hygra@`9e71ce9` on the published synthetic operator intake. See `hygra/README.md`.
- File format: `data/imported/SCHEMA.md`.
- Regenerator: `python numerical/export_cem_snapshots.py` (writes only into this repository).

No live coupling. Static snapshots only.

## Why this first set
- Nilpotent / shift-like operators are classical near-extremal examples for Crouzeix ratios.
- Real CEM operators keep numerical scouting grounded in the actual design problems the results are intended to serve.
- Small dimension keeps Lean formalization and ratio computation tractable while the abstract theory is developed.
