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
| `2026-08-16-cb-large/` | Large cb campaign (`k ≥ 8`, `degree ≥ 3`). Re-run with `python numerical/ratio_harness.py --large-cb`. |
| `2026-08-16-imported/` | Ratios on the first Torquon-GB / Hygra static snapshots (`--imported`). |
