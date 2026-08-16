# Contributing

## Agent rules
1. All formalization, numerical work, and theoretical notes stay inside this repository.
2. Read-only access to CEM repositories is permitted for realistic operator examples.
3. Never write to CEM repositories.
4. Prefer synthetic or anonymized matrices when possible. Imported data goes only into `data/imported/`.
5. Lean code must be mathlib-compatible. Prefer small, checkable lemmas.
6. Numerical scripts must be reproducible (seeded random generation, clear matrix sources).

## Data import convention
- Place static snapshots under `data/imported/<cem-name>/`.
- Include a short `README.md` in each imported folder describing origin, date, and any anonymization.
- Do not commit large binary files without git-lfs.

## Lean style
- One major statement per file when practical.
- Explicit `sorry` or open goals must be marked with a comment explaining the missing step.
- Prefer statements that can be checked by `lake build`.
