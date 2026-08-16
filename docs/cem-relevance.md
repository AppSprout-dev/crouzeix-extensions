# Relevance to AppSprout CEMs

- **Torquon-GB**: non-normal stiffness / transfer / damping matrices under tolerances and asymmetric loading. Scalar bound 2 already usable for transient and vibration matrix functions. cb / joint results would cover simultaneous treatment of multiple stage operators.
- **Phenara**: structural + thermal + multi-body operators. Joint spectral-set bounds map directly onto multi-physics phenotype evaluation.
- **Cultivation infrastructure**: multi-zone environmental Jacobians. Nearly-commuting families are realistic targets for early joint results.
- **Hybrid U-NSGA-III loops**: tighter residual and matrix-function bounds improve adaptive local search and surrogate refinement.

Any settled lemma is documented with a short “how to cite / use” note so CEM agents can optionally apply it.

## How to cite / use (2026-08-16)

- **Scalar constant 2 (universal).** Already settled. CEM evaluation
  pipelines may use `‖f(A)‖ ≤ 2 ‖f‖_{W(A)}` for any matrix function
  holomorphic near the numerical range. No result in this repository is
  required for that citation (Jin; Lorist–Schwenninger).
- **2×2 nilpotent sharpness.** `lean/NilpotentShift.lean` records that
  the unweighted 2×2 Jordan block attains the constant 2 for `p(z)=z`.
  Use this as a regression test for any CEM residual / matrix-function
  estimator: the estimator must not claim a universal constant `< 2`.
- **Disk operators.** If a CEM matrix is known (or certified) to have
  disk numerical range — including any unweighted nilpotent Jordan
  block, and more generally any 2-nilpotent matrix — the *complete*
  bound 2 is classical. That is the right citation for simultaneous
  treatment of several holomorphic functions of one such operator.
- **Nearly-normal CEM blocks** (synthetic stiffness / Jacobian
  stand-ins in the 2026-08-16 scout) produced scalar and cb probe
  ratios indistinguishable from 1. The universal 2 is very conservative
  for those families; a non-normality-dependent improvement (open
  problem 3) would be the high-value CEM result.

No automatic dependency is created. CEM agents should copy constants
and lemma names from this repository, not import it as a package.
