# Experiments

Dated numerical campaigns. Each folder should contain at least:

- `ratios.csv` — one row per (matrix, polynomial, method)
- `summary.md` — human-readable interpretation

Matrices themselves are *not* stored as binaries (`.npy` / `.npz` are
gitignored). Regenerate them from `../data/synthetic/manifest.json` and
`../numerical/ensembles.py`.

| folder | what |
|--------|------|
| `2026-08-16-baseline/` | First scout: Johnson vs legacy Monte-Carlo, nilpotent family, cb probes. |
