# Agent system context for crouzeix-extensions

You are working inside the isolated research repository AppSprout-dev/crouzeix-extensions.

## Core mission
Advance the completely-bounded analogue of Crouzeix’s theorem (constant 2) and multi-operator / joint spectral-set extensions. Produce Lean-checked lemmas and numerical evidence. Keep all work inside this repository.

## Isolation (non-negotiable)
- Read-only awareness of AppSprout CEM repositories (Torquon-GB, Phenara, Unsga3, CannaSage, etc.) is allowed for realistic operator examples and numerical-range samples.
- You must never open PRs, edit files, or create issues in any CEM repository.
- Settled results may be documented here so that CEM agents can optionally cite them; no automatic dependency is created.

## Sibling CEM operators (examples only)
- Torquon-GB: gearbox stiffness, transfer, damping matrices.
- Phenara: structural, thermal, multi-body, manufacturing operators.
- Cultivation: multi-zone environmental Jacobians.

## Current status
- Scalar Crouzeix theorem: settled at constant 2 (Jin; Lorist–Schwenninger, Aug 2026).
- Completely-bounded version with constant 2: open.
- Multi-operator / joint spectral sets: open.
- 2026-08-16: Johnson harness + first scout (max scalar/cb probe ratio = 2.0000).
  Lean: `NilpotentShift.scalar_monomial_ratio_eq_two`. Unweighted Jordan
  nilpotents reduce to the classical disk theorem; next open classes are
  perturbed nilpotents and weighted shifts. See `docs/notes/2026-08-16-first-session.md`.

## Preferred workflow
1. Numerical scouting on synthetic + imported matrices.
2. Special-class proofs (nilpotent shifts, weighted shifts, low-dimensional blocks).
3. Abstract dilation / completely-positive arguments.
4. Lean formalization of every settled claim.
5. Clear documentation of any result that CEM agents may later use.

## References
- Lorist & Schwenninger, arXiv:2608.03841
- Jin, “The Numerical Range Is a 2-Spectral Set” (2026)
- Crouzeix–Palencia (complete 1+√2)
