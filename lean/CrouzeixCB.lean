/-
  Completely-bounded Crouzeix conjecture (open) and the first special class.

  Companion file `NilpotentShift.lean` contains the first non-trivial
  Lean-checked lemmas: the 2×2 nilpotent Jordan block has scalar ratio
  exactly 2 for p(z) = z.
-/

import Mathlib

/-!
# Completely-bounded Crouzeix

The ordinary (scalar) Crouzeix theorem is settled (constant 2: Jin, July 2026;
Lorist–Schwenninger, arXiv:2608.03841). The completely-bounded analogue with
the same constant remains open.

## Status of the first special class

The unweighted nilpotent Jordan block `S_n` has numerical range equal to the
closed disk of radius `cos(π/(n+1))`. A disk is a *complete* 2-spectral set
by the Okubo–Ando / Berger–Stampfli / Holbrook dilation of numerical
contractions. Consequently the sharp cb statement for this family is
classical, once the disk theorem is available in Lean.

What is formalized now:

* `NilpotentShift.scalar_monomial_ratio_eq_two` — `‖S₂‖ / w(S₂) = 2`.
* `NilpotentShift.jordanNilpotent2_sq` — `S₂² = 0`.
* `NilpotentShift.abs_rayleigh_le_half` — `W(S₂) ⊆ { |z| ≤ 1/2 }`.

What remains (`sorry`, marked below):

* the disk ⇒ complete 2-spectral theorem;
* the identification `W(S_n) = disk(0, cos(π/(n+1)))` for `n > 2`;
* the cb statement for *perturbed* nilpotents and weighted shifts, whose
  numerical ranges are no longer disks (the first genuinely open special
  classes in this campaign).
-/

namespace CrouzeixCB

open Matrix

/-- Euclidean numerical range of a square complex matrix. -/
def numericalRange {n : Type*} [Fintype n] (A : Matrix n n ℂ) : Set ℂ :=
  { z | ∃ x : n → ℂ,
      Real.sqrt (∑ i, ‖x i‖ ^ 2) = 1 ∧
        z = star x ⬝ᵥ A.mulVec x }

/-- Completely-bounded Crouzeix conjecture (open).

  Informal statement: for every square matrix `A` and every matrix-valued
  polynomial `F`,
  `‖F(A)‖ ≤ 2 · sup_{z ∈ W(A)} ‖F(z)‖`.

  The definitions of the matrix-valued functional calculus and of the
  completely-bounded norm are not yet in this file; the proposition below
  is a named open goal, not a claim of proof. -/
theorem completely_bounded_crouzeix_conjecture : True := by
  -- Open. Replace `True` with the precise inequality once the
  -- matrix-valued calculus and cb-norm are defined.
  trivial

/-- Classical disk theorem (not yet formalized).

  If `W(A)` is contained in a closed disk of radius `r`, then that disk
  is a complete 2-spectral set for `A`. References: Okubo–Ando, Berger–
  Stampfli, Holbrook.

  **Missing step:** a Lean construction of the 2-dilation of a numerical
  contraction, or an equivalent completely-positive argument. -/
theorem disk_is_complete_two_spectral : True := by
  -- sorry in spirit — kept as `True` until the dilation infrastructure
  -- exists. Do not treat this as a proved theorem.
  trivial

/-- Unweighted nilpotent Jordan blocks: cb=2 reduces to the disk theorem.

  For the n-dimensional nilpotent shift `S_n`, `W(S_n)` is the disk of
  radius `cos(π/(n+1))`. The n=2 case of the radius (and of scalar
  sharpness) is proved in `NilpotentShift`. The complete bound itself
  waits on `disk_is_complete_two_spectral`. -/
theorem cb_for_nilpotent_shifts : True := by
  -- Open as a Lean theorem; mathematically conditional on the disk theorem.
  trivial

/-- Next special-class target: controlled perturbations of a nilpotent shift.

  `S_n + εE` has numerical range that is *not* in general a disk, so the
  disk theorem does not apply. This is the first class in the campaign
  whose cb=2 statement is not classical. -/
theorem cb_for_perturbed_nilpotent_shifts : True := by
  -- Open. Numerical scouting: `experiments/2026-08-16-baseline/`.
  trivial

/-- Next special-class target: weighted shifts (transport-like).

  Typical numerical ranges are elliptical or more complicated, not disks.
  Models directed coupling in CEM Jacobians. -/
theorem cb_for_weighted_shifts : True := by
  -- Open.
  trivial

end CrouzeixCB
