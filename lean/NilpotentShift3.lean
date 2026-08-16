/-
  The 3×3 nilpotent Jordan block has numerical range equal to the closed
  disk of radius cos(π/4) = cos(π/(3+1)).

  Inclusion W ⊆ disk is elementary (Cauchy–Schwarz + AM-GM). The reverse
  inclusion uses rotational symmetry of W and convexity (Toeplitz–Hausdorff).
  Those two steps are named `sorry`s.
-/

import CrouzeixCB
import NilpotentShift

open scoped BigOperators
open Matrix Complex
open CrouzeixCB
open CrouzeixCB.NilpotentShift

namespace CrouzeixCB
namespace NilpotentShift3

/-- The 3×3 nilpotent Jordan block `[[0,1,0],[0,0,1],[0,0,0]]`. -/
def jordanNilpotent3 : Matrix (Fin 3) (Fin 3) ℂ :=
  Matrix.of fun i j => if (j : ℕ) = (i : ℕ) + 1 then 1 else 0

lemma jordanNilpotent3_mulVec (x : Fin 3 → ℂ) :
    jordanNilpotent3.mulVec x 0 = x 1 ∧
      jordanNilpotent3.mulVec x 1 = x 2 ∧
      jordanNilpotent3.mulVec x 2 = 0 := by
  have h : ∀ i j : Fin 3, jordanNilpotent3 i j = if (j : ℕ) = (i : ℕ) + 1 then 1 else 0 := by
    intro i j; simp [jordanNilpotent3, Matrix.of_apply]
  refine ⟨?_, ?_, ?_⟩
  · simp [Matrix.mulVec, dotProduct, Fin.sum_univ_three, h]
  · simp [Matrix.mulVec, dotProduct, Fin.sum_univ_three, h]
  · simp [Matrix.mulVec, dotProduct, Fin.sum_univ_three, h]

lemma rayleigh_jordanNilpotent3 (x : Fin 3 → ℂ) :
    star x ⬝ᵥ jordanNilpotent3.mulVec x =
      star (x 0) * x 1 + star (x 1) * x 2 := by
  rw [dotProduct, Fin.sum_univ_three, (jordanNilpotent3_mulVec x).1,
    (jordanNilpotent3_mulVec x).2.1, (jordanNilpotent3_mulVec x).2.2,
    mul_zero, add_zero, Pi.star_apply, Pi.star_apply]

lemma abs_rayleigh_le_sum (x : Fin 3 → ℂ) :
    ‖star x ⬝ᵥ jordanNilpotent3.mulVec x‖ ≤
      ‖x 0‖ * ‖x 1‖ + ‖x 1‖ * ‖x 2‖ := by
  rw [rayleigh_jordanNilpotent3]
  refine (norm_add_le _ _).trans ?_
  simp [norm_mul, norm_star]

/-- `b √(1 − b²) ≤ 1/2` for `b ∈ [0, 1]`, via `(2b² − 1)² ≥ 0`. -/
lemma b_sqrt_le_half {b : ℝ} (hb0 : 0 ≤ b) (hb1 : b ≤ 1) :
    b * Real.sqrt (1 - b ^ 2) ≤ 1 / 2 := by
  have h1b : 0 ≤ 1 - b ^ 2 := by nlinarith
  have hsq : (b * Real.sqrt (1 - b ^ 2)) ^ 2 = b ^ 2 * (1 - b ^ 2) := by
    rw [mul_pow, Real.sq_sqrt h1b]
  have hle : (b * Real.sqrt (1 - b ^ 2)) ^ 2 ≤ (1 / 2 : ℝ) ^ 2 := by
    rw [hsq]
    nlinarith [sq_nonneg (2 * b ^ 2 - 1)]
  have hnon : 0 ≤ b * Real.sqrt (1 - b ^ 2) :=
    mul_nonneg hb0 (Real.sqrt_nonneg _)
  nlinarith [sq_nonneg ((1 / 2 : ℝ) - b * Real.sqrt (1 - b ^ 2)),
    hle, hnon]

/-- `ab + bc ≤ √2 / 2` on the unit sphere `a² + b² + c² = 1`, `a,b,c ≥ 0`. -/
lemma ab_add_bc_le_radius {a b c : ℝ}
    (ha : 0 ≤ a) (hb : 0 ≤ b) (hc : 0 ≤ c)
    (hsum : a ^ 2 + b ^ 2 + c ^ 2 = 1) :
    a * b + b * c ≤ Real.sqrt 2 / 2 := by
  have hac : (a + c) ^ 2 ≤ 2 * (a ^ 2 + c ^ 2) := by
    nlinarith [sq_nonneg (a - c)]
  have hac_non : 0 ≤ a + c := add_nonneg ha hc
  have h2 : 0 ≤ a ^ 2 + c ^ 2 := add_nonneg (sq_nonneg a) (sq_nonneg c)
  have hcs : a + c ≤ Real.sqrt 2 * Real.sqrt (a ^ 2 + c ^ 2) := by
    have hsq2 : Real.sqrt 2 ^ 2 = 2 := Real.sq_sqrt (by positivity)
    have hL : 0 ≤ Real.sqrt 2 * Real.sqrt (a ^ 2 + c ^ 2) :=
      mul_nonneg (Real.sqrt_nonneg _) (Real.sqrt_nonneg _)
    nlinarith [Real.sq_sqrt h2, hac, hsq2, hac_non, hL]
  have habc : a * b + b * c = b * (a + c) := by ring
  have hb1 : b ≤ 1 := by
    have : b ^ 2 ≤ 1 := by nlinarith [sq_nonneg a, sq_nonneg c]
    nlinarith [sq_nonneg (1 - b), hb]
  have hac2 : a ^ 2 + c ^ 2 = 1 - b ^ 2 := by nlinarith
  calc
    a * b + b * c = b * (a + c) := habc
    _ ≤ b * (Real.sqrt 2 * Real.sqrt (a ^ 2 + c ^ 2)) :=
      mul_le_mul_of_nonneg_left hcs hb
    _ = Real.sqrt 2 * (b * Real.sqrt (1 - b ^ 2)) := by
      rw [hac2]; ring
    _ ≤ Real.sqrt 2 * (1 / 2) :=
      mul_le_mul_of_nonneg_left (b_sqrt_le_half hb hb1) (Real.sqrt_nonneg _)
    _ = Real.sqrt 2 / 2 := by ring

lemma radius_eq_cos_pi_div_four : Real.cos (Real.pi / 4) = Real.sqrt 2 / 2 :=
  Real.cos_pi_div_four

lemma radius_eq_formula : Real.cos (Real.pi / 4) = Real.cos (Real.pi / (3 + 1)) := by
  norm_num

/-- `W(S₃) ⊆` closed disk of radius `cos(π/4)`. -/
theorem abs_rayleigh_le_cos_pi_div_four {x : Fin 3 → ℂ} (hx : eNorm x = 1) :
    ‖star x ⬝ᵥ jordanNilpotent3.mulVec x‖ ≤ Real.cos (Real.pi / 4) := by
  have hsum : ‖x 0‖ ^ 2 + ‖x 1‖ ^ 2 + ‖x 2‖ ^ 2 = 1 := by
    have := eNorm_sq x
    rw [hx, one_pow] at this
    simpa [Fin.sum_univ_three] using this.symm
  rw [radius_eq_cos_pi_div_four]
  refine (abs_rayleigh_le_sum x).trans ?_
  exact ab_add_bc_le_radius (norm_nonneg _) (norm_nonneg _) (norm_nonneg _) hsum

theorem numericalRange_subset_closedDisk :
    numericalRange jordanNilpotent3 ⊆ closedDisk (Real.cos (Real.pi / 4)) := by
  intro z hz
  rcases hz with ⟨x, hx, rfl⟩
  exact abs_rayleigh_le_cos_pi_div_four hx

/-- Standard basis vector `e₀ = (1, 0, 0)`. -/
def e0 : Fin 3 → ℂ := fun i => if i = 0 then 1 else 0

lemma eNorm_e0 : eNorm e0 = 1 := by
  simp [eNorm, e0, Fin.sum_univ_three]

lemma zero_mem_numericalRange : (0 : ℂ) ∈ numericalRange jordanNilpotent3 := by
  refine ⟨e0, eNorm_e0, ?_⟩
  rw [rayleigh_jordanNilpotent3]
  simp [e0]

/-- Unit vector attaining the numerical radius on the positive real axis. -/
noncomputable def attainRadius : Fin 3 → ℂ :=
  ![((1 / 2 : ℝ) : ℂ), ((Real.sqrt 2 / 2 : ℝ) : ℂ), ((1 / 2 : ℝ) : ℂ)]

lemma attainRadius_zero : attainRadius 0 = ((1 / 2 : ℝ) : ℂ) := by
  simp [attainRadius]

lemma attainRadius_one : attainRadius 1 = ((Real.sqrt 2 / 2 : ℝ) : ℂ) := by
  simp [attainRadius]

lemma attainRadius_two : attainRadius 2 = ((1 / 2 : ℝ) : ℂ) := by
  simp [attainRadius]

lemma attainRadius_norm_zero : ‖attainRadius 0‖ = 1 / 2 := by
  have hr : 0 ≤ (1 / 2 : ℝ) := by norm_num
  rw [attainRadius_zero]
  exact Complex.norm_of_nonneg hr

lemma attainRadius_norm_one : ‖attainRadius 1‖ = Real.sqrt 2 / 2 := by
  have hr : 0 ≤ Real.sqrt 2 / 2 := div_nonneg (Real.sqrt_nonneg _) (by norm_num)
  rw [attainRadius_one]
  exact Complex.norm_of_nonneg hr

lemma attainRadius_norm_two : ‖attainRadius 2‖ = 1 / 2 := by
  have hr : 0 ≤ (1 / 2 : ℝ) := by norm_num
  rw [attainRadius_two]
  exact Complex.norm_of_nonneg hr

lemma eNorm_attainRadius : eNorm attainRadius = 1 := by
  have hsq : (1 / 2 : ℝ) ^ 2 + (Real.sqrt 2 / 2) ^ 2 + (1 / 2 : ℝ) ^ 2 = 1 := by
    have : (Real.sqrt 2 / 2) ^ 2 = (2 : ℝ) / 4 := by
      rw [div_pow, Real.sq_sqrt (by norm_num : (0 : ℝ) ≤ 2)]
      norm_num
    rw [this]
    norm_num
  simp only [eNorm, Fin.sum_univ_three, attainRadius_norm_zero, attainRadius_norm_one,
    attainRadius_norm_two]
  rw [hsq]
  exact Real.sqrt_one

lemma rayleigh_attainRadius :
    star attainRadius ⬝ᵥ jordanNilpotent3.mulVec attainRadius =
      ((Real.sqrt 2 / 2 : ℝ) : ℂ) := by
  rw [rayleigh_jordanNilpotent3, attainRadius_zero, attainRadius_one, attainRadius_two]
  have hs0 : star ((1 / 2 : ℝ) : ℂ) = ((1 / 2 : ℝ) : ℂ) := by simp [conj_ofReal]
  have hs1 : star ((Real.sqrt 2 / 2 : ℝ) : ℂ) = ((Real.sqrt 2 / 2 : ℝ) : ℂ) := by
    simp [conj_ofReal]
  rw [hs0, hs1]
  have hR : (1 / 2 : ℝ) * (Real.sqrt 2 / 2) + (Real.sqrt 2 / 2) * (1 / 2 : ℝ) =
      Real.sqrt 2 / 2 := by ring
  calc
    ((1 / 2 : ℝ) : ℂ) * ((Real.sqrt 2 / 2 : ℝ) : ℂ) +
        ((Real.sqrt 2 / 2 : ℝ) : ℂ) * ((1 / 2 : ℝ) : ℂ)
      = ↑((1 / 2 : ℝ) * (Real.sqrt 2 / 2) + (Real.sqrt 2 / 2) * (1 / 2 : ℝ)) := by
        simp [ofReal_mul, ofReal_add]
    _ = ↑(Real.sqrt 2 / 2) := by rw [hR]

lemma radius_mem_numericalRange :
    (↑(Real.cos (Real.pi / 4)) : ℂ) ∈ numericalRange jordanNilpotent3 := by
  refine ⟨attainRadius, eNorm_attainRadius, ?_⟩
  rw [rayleigh_attainRadius, radius_eq_cos_pi_div_four]

/-- Diagonal phase rotation of a vector: `(y_j) = e^{i φ j} x_j`. -/
noncomputable def rotateVec (φ : ℝ) (x : Fin 3 → ℂ) : Fin 3 → ℂ :=
  fun i => Complex.exp (Complex.I * (φ * (i.val : ℝ))) * x i

lemma norm_phase (φ : ℝ) (t : ℝ) :
    ‖Complex.exp (Complex.I * (φ * t))‖ = 1 := by
  have h : Complex.I * (φ * t : ℂ) = (φ * t : ℝ) * Complex.I := by
    simp [mul_comm]
  simpa [h] using Complex.norm_exp_ofReal_mul_I (φ * t)

lemma eNorm_rotate (φ : ℝ) (x : Fin 3 → ℂ) :
    eNorm (rotateVec φ x) = eNorm x := by
  simp only [eNorm, rotateVec]
  refine congrArg Real.sqrt (Finset.sum_congr rfl fun i _ => ?_)
  rw [norm_mul, norm_phase, one_mul]

/-- Phase calculation: `⟨S (U_φ x), U_φ x⟩ = e^{iφ} ⟨S x, x⟩`.

**Missing step:** expand the three Rayleigh terms using `|e^{iθ}|=1` and
`conj(e^{iφ}) e^{2iφ} = e^{iφ}`. -/
lemma rayleigh_rotate (φ : ℝ) (x : Fin 3 → ℂ) :
    star (rotateVec φ x) ⬝ᵥ jordanNilpotent3.mulVec (rotateVec φ x) =
      Complex.exp (Complex.I * φ) * (star x ⬝ᵥ jordanNilpotent3.mulVec x) := by
  sorry

lemma rotate_mem {z : ℂ} (hz : z ∈ numericalRange jordanNilpotent3) (φ : ℝ) :
    Complex.exp (Complex.I * φ) * z ∈ numericalRange jordanNilpotent3 := by
  rcases hz with ⟨x, hx, rfl⟩
  refine ⟨rotateVec φ x, ?_, ?_⟩
  · exact (eNorm_rotate φ x).trans hx
  · exact (rayleigh_rotate φ x).symm

/-- Toeplitz–Hausdorff: the numerical range is convex.

**Missing step:** the classical convexity theorem (or a direct 3-dimensional
argument). Needed only for the reverse inclusion `disk ⊆ W(S₃)`. -/
theorem numericalRange_convex : Convex ℝ (numericalRange jordanNilpotent3) := by
  sorry

/-- `closed disk ⊆ W(S₃)`. Uses rotational symmetry and convexity.

**Missing step:** identify an arbitrary `w` with `|w| ≤ cos(π/4)` as the
convex combination of `0` and the rotated radius point
`e^{i arg w} · cos(π/4)`. Depends on `numericalRange_convex` and
`rayleigh_rotate`. -/
theorem closedDisk_subset_numericalRange :
    closedDisk (Real.cos (Real.pi / 4)) ⊆ numericalRange jordanNilpotent3 := by
  intro w hw
  by_cases h0 : w = 0
  · simpa [h0] using zero_mem_numericalRange
  · sorry

/-- `W(S₃) =` closed disk of radius `cos(π/4) = cos(π/(3+1))`. -/
theorem numericalRange_eq_disk :
    numericalRange jordanNilpotent3 = closedDisk (Real.cos (Real.pi / 4)) :=
  subset_antisymm numericalRange_subset_closedDisk closedDisk_subset_numericalRange

end NilpotentShift3
end CrouzeixCB
