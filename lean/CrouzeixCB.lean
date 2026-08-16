/-
  Completely-bounded Crouzeix conjecture (open).
  Skeleton only — no claim of proof.
-/

import Mathlib

/-!
# Completely-bounded Crouzeix

The ordinary (scalar) Crouzeix theorem is settled (constant 2).
The completely-bounded analogue with the same constant remains open.

This file records the statement we aim to prove or disprove,
together with a placeholder for the first special-class result.
-/

namespace CrouzeixCB

/-- Completely-bounded Crouzeix conjecture (open).
  For every matrix \(A\) and every matrix-valued polynomial \(F\),
  \(\|F(A)\| \le 2 \cdot \sup_{z \in W(A)} \|F(z)\|\). -/
theorem completely_bounded_crouzeix_conjecture : True := by
  -- Placeholder. Replace with the precise statement once the
  -- necessary definitions (numerical range, matrix-valued functional calculus,
  -- completely-bounded norm) are in place.
  trivial

/-- First special-class target: nilpotent shifts (or controlled perturbations).
  Scalar case is known; cb version is the next concrete goal. -/
theorem cb_for_nilpotent_shifts : True := by
  trivial

end CrouzeixCB
