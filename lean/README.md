# Lean 4 formalization

Target: mathlib-compatible statements of the completely-bounded Crouzeix
conjecture and related special-class results.

## Current files
- `CrouzeixCB.lean` — open cb conjecture, named disk-theorem goal, and the
  next special-class targets (perturbed nilpotents, weighted shifts).
- `NilpotentShift.lean` — first non-placeholder lemmas: the 2×2 nilpotent
  Jordan block has `S² = 0`, `W(S) ⊆ {|z| ≤ 1/2}`, `‖S‖ = 1`, and the
  scalar ratio of `p(z) = z` is exactly 2.

## What is proved vs open
Proved (elementary, no dilation theory):
- `NilpotentShift.jordanNilpotent2_sq`
- `NilpotentShift.abs_rayleigh_le_half`
- `NilpotentShift.eNorm_mulVec_le` + attaining vector `e1`
- `NilpotentShift.scalar_monomial_ratio_eq_two`

Open / recorded as `True` placeholders (do **not** treat as theorems):
- `completely_bounded_crouzeix_conjecture`
- `disk_is_complete_two_spectral` (classical; missing Lean dilation)
- `cb_for_nilpotent_shifts` (mathematically reduces to the disk theorem)
- `cb_for_perturbed_nilpotent_shifts`, `cb_for_weighted_shifts`

The unweighted Jordan nilpotent has disk numerical range, so its cb=2
statement is classical once the disk theorem is formalized. Perturbed
nilpotents and weighted shifts are the first classes whose numerical
ranges are not disks.

## Build
Requires a standard mathlib setup (`elan` + `lake`). This repository does
not yet pin a `lakefile.toml` / `lean-toolchain`; add those as the
formalization matures.

```bash
lake build
```

No Lean toolchain is assumed in the default agent environment; treat the
lemmas as ready for a local `lake build`, not as already CI-checked.
