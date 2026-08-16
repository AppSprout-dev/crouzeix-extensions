# crouzeix-extensions

Isolated research repository for the completely-bounded analogue of Crouzeix’s theorem and multi-operator / joint spectral-set extensions.

**Status (August 2026)**  
The ordinary (scalar) Crouzeix theorem is settled: for any bounded operator \(A\) and any function \(f\) analytic near the closure of the numerical range \(W(A)\),
\[
\|f(A)\| \le 2 \sup_{z \in W(A)} |f(z)|.
\]
The constant 2 is sharp. Independent proofs: Jin (July 2026) and Lorist–Schwenninger (arXiv:2608.03841).

The completely-bounded (cb) version with the same constant and multi-operator / joint spectral-set extensions remain **open**.

First-session log (2026-08-16): Johnson numerical scout in
`experiments/2026-08-16-baseline/` (max observed scalar and cb-probe
ratios = 2.0000) and the first Lean lemmas in `lean/NilpotentShift.lean`.
See `docs/notes/2026-08-16-first-session.md`.

## Isolation rules
- This repository is independent of the AppSprout CEM repositories (Torquon-GB, Phenara, Unsga3, CannaSage, etc.).
- Agents here may **read** public or explicitly shared operator logs, numerical-range samples, and matrix ensembles from the CEM repositories.
- Agents here must **not** open pull requests, modify files, or create issues in any CEM repository.
- Agents in the CEM repositories may **read** settled theorems, Lean lemmas, and documented constants from this repository.
- No Git submodules, package dependencies, or shared build steps that create tight coupling.
- Any imported CEM data lives under `data/imported/` as static snapshots.

## Sibling CEM context (read-only awareness)
- **Torquon-GB**: gearbox stage stiffness / transfer / damping matrices under tolerances.
- **Phenara**: structural operators, multi-body transfer maps, manufacturing-process operators for space-economy systems.
- **Cultivation / CannaSage**: environmental-control and multi-zone Jacobians.
- **Unsga3**: multi-objective evolutionary framework used in hybrid loops with the above.

## Immediate engineering value
Settled scalar bounds (constant 2) can already be used inside CEM evaluation pipelines for residual control, matrix-function error estimates, and adaptive tolerances. Any progress on the cb or joint versions will strengthen multi-physics evaluation layers.

## Repository layout
- `docs/` — attack plan, open problems, CEM relevance notes
- `lean/` — Lean 4 formalization (mathlib)
- `numerical/` — Python / Julia scouting scripts
- `data/` — imported CEM snapshots + synthetic test matrices
- `experiments/` — notebooks and ratio computations

## How to contribute
See `CONTRIBUTING.md`. All work stays inside this repository until a result is settled and documented for optional use by the CEMs.
