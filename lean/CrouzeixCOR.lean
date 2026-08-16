/-
  Clouâtre–Ostermann–Ransford (COR) reduction for the completely-bounded
  Crouzeix problem.

  This file is the first *complete* (matrix-valued) milestone: the algebraic
  COR 1+√2 bound, which does not use commutativity of θ(f) with θ(α(f)).

  Companion: `CrouzeixCB.lean` keeps the open constant-2 statement.
-/

import CrouzeixCB

open scoped Kronecker
open Matrix Complex CrouzeixCB

/-!
# COR route (commutativity-free)

Lorist–Schwenninger (arXiv:2608.03841, Remark 4(5)) and Jin settle the
*scalar* Crouzeix theorem at constant 2. Both proofs fail after matrix
amplification: LS Lemma 1 needs `Eₙ = θ(α(fⁿ))` to commute with
`T = θ(f)`, which holds in a commutative uniform algebra and fails in
`Mₖ(𝒜)`.

The replacement target is COR Conjecture 1.1(ii)
(J. Operator Theory 90 (2023)):

*Let `𝒜` be a uniform algebra, `α : 𝒜 → 𝒜` a unital antilinear complete
contraction, `θ : 𝒜 → B(H)` a unital homomorphism, and
`Λ := θ + θ ∘ α(·)∗` with `‖Λ‖_cb ≤ 2`. Then `‖θ‖_cb ≤ 2`.*

Known, and commutativity-free:

* scalar `‖θ‖ ≤ 2` — LS Remark 4(4), via Arveson–Stinespring;
* `‖θ‖_cb ≤ 1+√2` — COR Theorem 1.1 / Proposition 6.2
  (the same quartic estimate on every ampliation).

The four Lean steps, none of which needs `[T, Eₙ] = 0`:

1. matrix-valued calculus `F(A) = Σ Cⱼ ⊗ Aʲ` (already `evalMatrixPoly`);
2. double-layer `Φ` unital CP ⇒ `‖Λ‖_cb = 2` (analytic; named open);
3. `α` a complete contraction on convex `Ω` (analytic; named open);
4. **this file:** the COR quartic `κ⁴ ≤ 2κ³ + κ² ⇒ κ ≤ 1+√2`, which is
   the complete `1+√2` milestone, and the open constant-2 target.

Crouzeix–Palencia’s complete `1+√2` is **not** a settlement of the
constant-2 conjecture. The constant-2 statement remains COR 1.1(ii).
-/

namespace CrouzeixCB
namespace COR

/-- COR quartic. If `κ ≥ 0` and `κ⁴ ≤ 2κ³ + κ²`, then `κ ≤ 1 + √2`.

This is the only analytic estimate in the COR 1+√2 argument
(Theorem 1.1): after using `‖θ_α‖ ≤ 1` and that `α` is a contraction,
the homomorphism norm satisfies the quartic, hence is at most `1+√2`.
The same quartic applies to every ampliation, so the bound is complete.
No commutativity is used. -/
theorem cor_quartic_bound {κ : ℝ} (hκ : 0 ≤ κ)
    (h : κ ^ 4 ≤ 2 * κ ^ 3 + κ ^ 2) : κ ≤ 1 + Real.sqrt 2 := by
  have hquad : κ ^ 2 - 2 * κ - 1 ≤ 0 := by
    nlinarith [sq_nonneg κ]
  have hsq : (κ - 1) ^ 2 ≤ 2 := by
    have : (κ - 1) ^ 2 = κ ^ 2 - 2 * κ + 1 := by ring
    linarith
  have hnn : 0 ≤ Real.sqrt 2 := Real.sqrt_nonneg _
  have habs : |κ - 1| ≤ Real.sqrt 2 := by
    rw [← sq_le_sq₀ (abs_nonneg (κ - 1)) hnn, sq_abs,
      Real.sq_sqrt (by norm_num : (0 : ℝ) ≤ 2)]
    exact hsq
  have : κ - 1 ≤ Real.sqrt 2 := (abs_le.mp habs).2
  linarith

/-- Package: a complete double-layer estimate produces the COR quartic
on the homomorphism norm `κ`, hence `κ ≤ 1+√2`.

`h` is the output of COR’s estimate
`‖θ(f)‖⁴ ≤ 2‖θ‖³ + ‖θ‖²` (for `‖f‖ ≤ 1`) after taking the supremum.
That estimate uses `‖Λ‖_cb ≤ 2` and that `α` is a complete contraction;
it does **not** use commutativity of `θ(f)` with `θ(α(f))`. -/
theorem complete_one_add_sqrt_two_of_quartic {κ : ℝ} (hκ : 0 ≤ κ)
    (h : κ ^ 4 ≤ 2 * κ ^ 3 + κ ^ 2) : κ ≤ 1 + Real.sqrt 2 :=
  cor_quartic_bound hκ h

/-- Linear pencils: `F(z) = C₀ + C₁ z` evaluates as `C₀ ⊗ I + C₁ ⊗ A`. -/
theorem evalMatrixPoly_linear
    {k n : Type*} [Fintype k] [Fintype n] [DecidableEq k] [DecidableEq n]
    (C0 C1 : Matrix k k ℂ) (A : Matrix n n ℂ) :
    evalMatrixPoly [C0, C1] A = C0 ⊗ₖ (1 : Matrix n n ℂ) + C1 ⊗ₖ A := by
  simp [evalMatrixPoly, evalMatrixPoly.go]

/-- Constant polynomials: `eval (C) A = C ⊗ I`. -/
theorem evalMatrixPoly_const
    {k n : Type*} [Fintype k] [Fintype n] [DecidableEq k] [DecidableEq n]
    (C : Matrix k k ℂ) (A : Matrix n n ℂ) :
    evalMatrixPoly [C] A = C ⊗ₖ (1 : Matrix n n ℂ) := by
  simp [evalMatrixPoly, evalMatrixPoly.go]

/-- The Kronecker calculus is a homomorphism on constant polynomials. -/
theorem evalMatrixPoly_const_mul
    {k n : Type*} [Fintype k] [Fintype n] [DecidableEq k] [DecidableEq n]
    (C D : Matrix k k ℂ) (A : Matrix n n ℂ) :
    evalMatrixPoly [C] A * evalMatrixPoly [D] A =
      evalMatrixPoly [C * D] A := by
  simp only [evalMatrixPoly_const]
  rw [← mul_kronecker_mul, one_mul]

/-- Amplification `F(z) = z I_k` is the Kronecker embedding of `A`. -/
theorem evalMatrixPoly_zIk
    {k n : Type*} [Fintype k] [Fintype n] [DecidableEq k] [DecidableEq n]
    (A : Matrix n n ℂ) :
    evalMatrixPoly [(0 : Matrix k k ℂ), (1 : Matrix k k ℂ)] A =
      (1 : Matrix k k ℂ) ⊗ₖ A := by
    rw [evalMatrixPoly_linear, zero_kronecker, zero_add]

/-- Complete Crouzeix–Palencia bound (constant `1+√2`).

  Informal: if the double-layer map `Φ` is unital completely positive
  and `α` is a complete contraction — the COR / Crouzeix–Palencia
  hypotheses, which do not require commutativity — then
  `‖F(A)‖ ≤ (1+√2) sup_{W(A)} ‖F‖`.

  The algebraic step is `complete_one_add_sqrt_two_of_quartic`.
  What remains is the construction of `Φ` and `α` on a convex
  neighbourhood of `W(A)` (double-layer potential / Cauchy transform).
  This is **not** a settlement of the constant-2 conjecture. -/
theorem complete_crouzeix_palencia
    {n k : Type*} [Fintype n] [Fintype k] [DecidableEq n] [DecidableEq k]
    (A : Matrix n n ℂ) (F : List (Matrix k k ℂ)) :
    opNorm (evalMatrixPoly F A) ≤
      (1 + Real.sqrt 2) *
        sSup ((fun z => opNorm (evalMatrixPolyAt F z)) '' numericalRange A) := by
  sorry -- missing: double-layer Φ unital CP and α complete contraction

/-- COR Conjecture 1.1(ii), specialised to the holomorphic calculus of `A`.

  This is the commutativity-free form of the completely-bounded Crouzeix
  conjecture with constant 2. It is open. Do not replace with `True`. -/
theorem cor_conjecture_cb_two
    {n k : Type*} [Fintype n] [Fintype k] [DecidableEq n] [DecidableEq k]
    (A : Matrix n n ℂ) (F : List (Matrix k k ℂ)) :
    opNorm (evalMatrixPoly F A) ≤
      2 * sSup ((fun z => opNorm (evalMatrixPolyAt F z)) '' numericalRange A) := by
  sorry -- open: COR 1.1(ii) / universal completely-bounded Crouzeix at 2

end COR
end CrouzeixCB
