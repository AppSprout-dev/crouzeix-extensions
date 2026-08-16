/-
  Completely-bounded Crouzeix conjecture (open) and the first special class.

  Companion files:
  * `NilpotentShift.lean` — 2×2 nilpotent sharpness (scalar ratio of z is 2).
  * `NilpotentShift3.lean` — `W(S₃) =` closed disk of radius `cos(π/4)`.
  * `CrouzeixCOR.lean` — COR 1+√2 quartic (sorry-free) and open cb=2 target.
-/

import Mathlib
import Mathlib.LinearAlgebra.Matrix.Kronecker

open scoped BigOperators Kronecker
open Matrix Complex

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
* `NilpotentShift3.numericalRange_eq_disk` — `W(S₃) = disk(0, cos(π/4))`
  (reverse inclusion uses named `sorry`s: Toeplitz–Hausdorff convexity and
  a phase-rotation identity).

What remains open:

* the disk ⇒ complete 2-spectral theorem;
* `cb_for_perturbed_nilpotent` below (`S_n + εE`, W not a disk);
* weighted shifts.
-/

namespace CrouzeixCB

/-- Euclidean (ℓ²) norm on `n → ℂ`. -/
noncomputable def euclNorm {n : Type*} [Fintype n] (x : n → ℂ) : ℝ :=
  Real.sqrt (∑ i, ‖x i‖ ^ 2)

/-- Operator norm induced by `euclNorm`. -/
noncomputable def opNorm {n : Type*} [Fintype n] (A : Matrix n n ℂ) : ℝ :=
  sSup { r | ∃ x : n → ℂ, euclNorm x = 1 ∧ r = euclNorm (A.mulVec x) }

/-- Euclidean numerical range of a square complex matrix. -/
def numericalRange {n : Type*} [Fintype n] (A : Matrix n n ℂ) : Set ℂ :=
  { z | ∃ x : n → ℂ,
      Real.sqrt (∑ i, ‖x i‖ ^ 2) = 1 ∧
        z = star x ⬝ᵥ A.mulVec x }

/-- Closed disk of radius `r` centred at the origin. -/
def closedDisk (r : ℝ) : Set ℂ := { z | ‖z‖ ≤ r }

/-- Unweighted nilpotent Jordan block of size `n` (1's on the superdiagonal). -/
def jordanNilpotent (n : ℕ) : Matrix (Fin n) (Fin n) ℂ :=
  Matrix.of fun i j => if (j : ℕ) = (i : ℕ) + 1 then 1 else 0

/-- Evaluate a matrix-valued polynomial `F(z) = Σ C_j z^j` at a scalar. -/
def evalMatrixPolyAt.go {k : Type*} [Fintype k] [DecidableEq k]
    (z : ℂ) : List (Matrix k k ℂ) → ℂ → Matrix k k ℂ
  | [], _ => 0
  | C :: rest, zp => zp • C + evalMatrixPolyAt.go z rest (zp * z)

def evalMatrixPolyAt {k : Type*} [Fintype k] [DecidableEq k]
    (F : List (Matrix k k ℂ)) (z : ℂ) : Matrix k k ℂ :=
  evalMatrixPolyAt.go z F 1

/-- `F(A) = Σ C_j ⊗ A^j` (Kronecker convention). -/
def evalMatrixPoly.go {k n : Type*} [Fintype k] [Fintype n] [DecidableEq k] [DecidableEq n]
    (A : Matrix n n ℂ) : List (Matrix k k ℂ) → Matrix n n ℂ → Matrix (k × n) (k × n) ℂ
  | [], _ => 0
  | C :: rest, Ap => C ⊗ₖ Ap + evalMatrixPoly.go A rest (Ap * A)

def evalMatrixPoly {k n : Type*} [Fintype k] [Fintype n] [DecidableEq k] [DecidableEq n]
    (F : List (Matrix k k ℂ)) (A : Matrix n n ℂ) : Matrix (k × n) (k × n) ℂ :=
  evalMatrixPoly.go A F 1

/-- Completely-bounded Crouzeix conjecture (open).

  Informal statement: for every square matrix `A` and every matrix-valued
  polynomial `F`,
  `‖F(A)‖ ≤ 2 · sup_{z ∈ W(A)} ‖F(z)‖`.

  The proposition below is a named open goal, not a claim of proof. -/
theorem completely_bounded_crouzeix_conjecture
    {n k : Type*} [Fintype n] [Fintype k] [DecidableEq n] [DecidableEq k]
    (A : Matrix n n ℂ) (F : List (Matrix k k ℂ)) :
    opNorm (evalMatrixPoly F A) ≤
      2 * sSup ((fun z => opNorm (evalMatrixPolyAt F z)) '' numericalRange A) := by
  sorry -- open: universal completely-bounded Crouzeix with constant 2

/-- Classical disk theorem (not yet formalized).

  If `W(A)` is contained in a closed disk of radius `r`, then that disk
  is a complete 2-spectral set for `A`. References: Okubo–Ando, Berger–
  Stampfli, Holbrook.

  **Missing step:** a Lean construction of the 2-dilation of a numerical
  contraction, or an equivalent completely-positive argument. -/
theorem disk_is_complete_two_spectral
    {n k : Type*} [Fintype n] [Fintype k] [DecidableEq n] [DecidableEq k]
    (A : Matrix n n ℂ) (r : ℝ) (hr : 0 ≤ r)
    (hW : numericalRange A ⊆ closedDisk r)
    (F : List (Matrix k k ℂ)) :
    opNorm (evalMatrixPoly F A) ≤
      2 * sSup ((fun z => opNorm (evalMatrixPolyAt F z)) '' numericalRange A) := by
  sorry -- missing: 2-dilation of a numerical contraction

/-- Unweighted nilpotent Jordan blocks: cb=2 reduces to the disk theorem.

  For the n-dimensional nilpotent shift `S_n`, `W(S_n)` is the disk of
  radius `cos(π/(n+1))`. The n=2 radius and n=3 disk equality are in
  `NilpotentShift` / `NilpotentShift3`. The complete bound itself waits
  on `disk_is_complete_two_spectral`. -/
theorem cb_for_nilpotent_shifts
    {n : ℕ} {k : Type*} [Fintype k] [DecidableEq k] [DecidableEq (Fin n)]
    (F : List (Matrix k k ℂ)) :
    opNorm (evalMatrixPoly F (jordanNilpotent n)) ≤
      2 * sSup ((fun z => opNorm (evalMatrixPolyAt F z)) ''
        numericalRange (jordanNilpotent n)) := by
  sorry -- conditional on disk_is_complete_two_spectral + W(S_n) = disk

/-- Open special-class statement: completely-bounded Crouzeix with constant 2
    for every perturbation `S_n + ε E` of a nilpotent Jordan block.

    `W(S_n + ε E)` is not a disk in general, so the classical disk theorem
    does not apply. No proof is claimed. -/
theorem cb_for_perturbed_nilpotent
    {n : ℕ} (ε : ℝ) (E : Matrix (Fin n) (Fin n) ℂ)
    {k : ℕ} (F : List (Matrix (Fin k) (Fin k) ℂ)) :
    opNorm (evalMatrixPoly F (jordanNilpotent n + ε • E)) ≤
      2 * sSup ((fun z => opNorm (evalMatrixPolyAt F z)) ''
        numericalRange (jordanNilpotent n + ε • E)) := by
  sorry -- open: first genuinely non-disk special class

/-- Next special-class target: weighted shifts (transport-like).

  Typical numerical ranges are elliptical or more complicated, not disks.
  Models directed coupling in CEM Jacobians. -/
theorem cb_for_weighted_shifts
    {n : ℕ} (weights : Fin n → ℂ)
    {k : Type*} [Fintype k] [DecidableEq k] [DecidableEq (Fin n)]
    (F : List (Matrix k k ℂ)) :
    let A : Matrix (Fin n) (Fin n) ℂ :=
      Matrix.of fun i j => if (j : ℕ) = (i : ℕ) + 1 then weights i else 0
    opNorm (evalMatrixPoly F A) ≤
      2 * sSup ((fun z => opNorm (evalMatrixPolyAt F z)) '' numericalRange A) := by
  sorry -- open: weighted-shift campaign, not this session

end CrouzeixCB
