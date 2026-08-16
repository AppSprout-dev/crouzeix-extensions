/-
  First special-class lemmas: the 2×2 nilpotent Jordan block.

  These are the first non-placeholder statements in the campaign.
  The scalar Crouzeix ratio of p(z) = z on this matrix is exactly 2
  (classical sharpness example). The completely-bounded statement for
  the unweighted nilpotent family reduces to the classical fact that a
  disk is a complete 2-spectral set; that reduction is recorded, not
  proved, in `CrouzeixCB.lean`.
-/

import Mathlib

open scoped BigOperators
open Matrix Complex

namespace CrouzeixCB
namespace NilpotentShift

/-- Euclidean (ℓ²) norm on `n → ℂ`. The default `Pi` norm is `∞`-norm. -/
noncomputable def eNorm {n : Type*} [Fintype n] (x : n → ℂ) : ℝ :=
  Real.sqrt (∑ i, ‖x i‖ ^ 2)

lemma eNorm_nonneg {n : Type*} [Fintype n] (x : n → ℂ) : 0 ≤ eNorm x :=
  Real.sqrt_nonneg _

lemma eNorm_sq {n : Type*} [Fintype n] (x : n → ℂ) :
    eNorm x ^ 2 = ∑ i, ‖x i‖ ^ 2 :=
  Real.sq_sqrt (Finset.sum_nonneg fun _ _ => sq_nonneg _)

/-- The 2×2 nilpotent Jordan block `[[0, 1], [0, 0]]`. -/
def jordanNilpotent2 : Matrix (Fin 2) (Fin 2) ℂ :=
  Matrix.of fun i j => if i = 0 ∧ j = 1 then 1 else 0

lemma jordanNilpotent2_apply :
    jordanNilpotent2 0 0 = 0 ∧ jordanNilpotent2 0 1 = 1 ∧
      jordanNilpotent2 1 0 = 0 ∧ jordanNilpotent2 1 1 = 0 := by
  simp [jordanNilpotent2, Matrix.of_apply]

lemma jordanNilpotent2_mulVec (x : Fin 2 → ℂ) :
    jordanNilpotent2.mulVec x 0 = x 1 ∧ jordanNilpotent2.mulVec x 1 = 0 := by
  constructor
  · simp [Matrix.mulVec_apply, jordanNilpotent2, Matrix.of_apply, Fin.sum_univ_two]
  · simp [Matrix.mulVec_apply, jordanNilpotent2, Matrix.of_apply, Fin.sum_univ_two]

/-- Index-2 nilpotence. -/
lemma jordanNilpotent2_sq : jordanNilpotent2 * jordanNilpotent2 = 0 := by
  ext i j
  fin_cases i <;> fin_cases j <;>
    simp [jordanNilpotent2, Matrix.mul_apply, Matrix.of_apply, Fin.sum_univ_two]

/-- Rayleigh quotient `⟨Sx, x⟩ = conj(x₀) x₁`. -/
lemma rayleigh_jordanNilpotent2 (x : Fin 2 → ℂ) :
    star x ⬝ᵥ jordanNilpotent2.mulVec x = star (x 0) * x 1 := by
  rw [dotProduct, Fin.sum_univ_two, (jordanNilpotent2_mulVec x).1,
    (jordanNilpotent2_mulVec x).2, mul_zero, add_zero, Pi.star_apply]

lemma abs_rayleigh_jordanNilpotent2 (x : Fin 2 → ℂ) :
    ‖star x ⬝ᵥ jordanNilpotent2.mulVec x‖ = ‖x 0‖ * ‖x 1‖ := by
  rw [rayleigh_jordanNilpotent2, norm_mul, norm_star]

/-- AM-GM: `ab ≤ (a² + b²)/2` for `a, b ≥ 0`. -/
lemma mul_le_mean_sq {a b : ℝ} (_ha : 0 ≤ a) (_hb : 0 ≤ b) :
    a * b ≤ (a ^ 2 + b ^ 2) / 2 := by
  have : 0 ≤ (a - b) ^ 2 := sq_nonneg (a - b)
  nlinarith

/-- Numerical-radius bound: `|⟨Sx, x⟩| ≤ 1/2` on the Euclidean unit sphere.

This is the inclusion `W(S) ⊆ {z | |z| ≤ 1/2}`. Combined with the matching
lower bound below, `w(S) = 1/2 = cos(π/3)`, as predicted by the disk formula
for the n-dimensional nilpotent Jordan block. -/
theorem abs_rayleigh_le_half {x : Fin 2 → ℂ} (hx : eNorm x = 1) :
    ‖star x ⬝ᵥ jordanNilpotent2.mulVec x‖ ≤ 1 / 2 := by
  have hsum : ‖x 0‖ ^ 2 + ‖x 1‖ ^ 2 = 1 := by
    have := eNorm_sq x
    rw [hx, one_pow] at this
    simpa [Fin.sum_univ_two] using this.symm
  rw [abs_rayleigh_jordanNilpotent2]
  have := mul_le_mean_sq (norm_nonneg (x 0)) (norm_nonneg (x 1))
  rwa [hsum] at this

/-- Operator-norm bound `‖Sx‖₂ ≤ ‖x‖₂`. -/
theorem eNorm_mulVec_le (x : Fin 2 → ℂ) :
    eNorm (jordanNilpotent2.mulVec x) ≤ eNorm x := by
  have h := jordanNilpotent2_mulVec x
  have hs : ∑ i : Fin 2, ‖jordanNilpotent2.mulVec x i‖ ^ 2 = ‖x 1‖ ^ 2 := by
    rw [Fin.sum_univ_two, h.1, h.2, norm_zero]
    ring
  have : eNorm (jordanNilpotent2.mulVec x) ^ 2 ≤ eNorm x ^ 2 := by
    rw [eNorm_sq, eNorm_sq, hs, Fin.sum_univ_two]
    nlinarith [sq_nonneg (‖x 0‖)]
  nlinarith [eNorm_nonneg (jordanNilpotent2.mulVec x), eNorm_nonneg x]

/-- Standard basis vector `e₁ = (0, 1)`. -/
def e1 : Fin 2 → ℂ := fun i => if i = 1 then 1 else 0

lemma eNorm_e1 : eNorm e1 = 1 := by
  simp [eNorm, e1, Fin.sum_univ_two]

lemma eNorm_S_e1 : eNorm (jordanNilpotent2.mulVec e1) = 1 := by
  have h := jordanNilpotent2_mulVec e1
  have he : e1 1 = 1 := by simp [e1]
  rw [eNorm, Fin.sum_univ_two, h.1, h.2, he, norm_one, norm_zero]
  norm_num

/-- Equal-weight unit vector that attains the numerical radius. -/
noncomputable def eqWeight : Fin 2 → ℂ :=
  fun _ => ((Real.sqrt 2)⁻¹ : ℝ)

lemma eqWeight_norm (i : Fin 2) : ‖eqWeight i‖ = (Real.sqrt 2)⁻¹ := by
  have hr : 0 ≤ (Real.sqrt 2)⁻¹ := inv_nonneg.2 (Real.sqrt_nonneg _)
  simpa [eqWeight] using Complex.norm_of_nonneg hr

lemma eNorm_eqWeight : eNorm eqWeight = 1 := by
  have hsq : ((Real.sqrt 2)⁻¹) ^ 2 = (1 / 2 : ℝ) := by
    rw [inv_pow, Real.sq_sqrt (by norm_num : (0 : ℝ) ≤ 2)]
    norm_num
  simp only [eNorm, Fin.sum_univ_two, eqWeight_norm]
  rw [hsq]
  norm_num

lemma rayleigh_eqWeight :
    star eqWeight ⬝ᵥ jordanNilpotent2.mulVec eqWeight = (↑(1 / 2 : ℝ) : ℂ) := by
  rw [rayleigh_jordanNilpotent2]
  have hstar : star (eqWeight 0) = eqWeight 0 := by
    simp [eqWeight, conj_ofReal]
  rw [hstar]
  simp only [eqWeight]
  have hR : ((Real.sqrt 2)⁻¹ : ℝ) * ((Real.sqrt 2)⁻¹ : ℝ) = (1 / 2 : ℝ) := by
    rw [← pow_two, inv_pow, Real.sq_sqrt (by norm_num : (0 : ℝ) ≤ 2)]
    norm_num
  rw [← ofReal_mul, hR]

/-- Scalar Crouzeix ratio of `p(z) = z` on the 2×2 nilpotent shift is exactly 2.

Recorded as the two sharp one-sided bounds:
* there is a unit vector with `‖Sx‖ = 1` (so the operator norm is ≥ 1, hence = 1
  by `eNorm_mulVec_le`);
* `|⟨Sx, x⟩| ≤ 1/2` on the unit sphere, with equality at `eqWeight`
  (so the numerical radius is exactly 1/2).

Thus `‖S‖ / w(S) = 2`, which is the classical sharpness example for Crouzeix. -/
theorem scalar_monomial_ratio_eq_two :
    (∃ x : Fin 2 → ℂ, eNorm x = 1 ∧ eNorm (jordanNilpotent2.mulVec x) = 1) ∧
      (∀ x : Fin 2 → ℂ, eNorm x = 1 →
        ‖star x ⬝ᵥ jordanNilpotent2.mulVec x‖ ≤ 1 / 2) ∧
      (∃ x : Fin 2 → ℂ, eNorm x = 1 ∧
        star x ⬝ᵥ jordanNilpotent2.mulVec x = (↑(1 / 2 : ℝ) : ℂ)) := by
  refine ⟨⟨e1, eNorm_e1, eNorm_S_e1⟩, ?_, ⟨eqWeight, eNorm_eqWeight, rayleigh_eqWeight⟩⟩
  intro x hx
  exact abs_rayleigh_le_half hx

end NilpotentShift
end CrouzeixCB
