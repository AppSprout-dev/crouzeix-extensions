# Lean 4 formalization

Target: mathlib-compatible statements of the completely-bounded Crouzeix
conjecture and related special-class results.

## Pin
- `lean-toolchain` — `leanprover/lean4:v4.34.0-rc1` (mathlib as of 2026-08-16)
- `lakefile.toml` — mathlib pinned at `274ed6d67d9b226c557813b9ce437574cccdce11`

This directory is the Lean project root.

```bash
cd lean
lake build NilpotentShift
lake build NilpotentShift3
lake build CrouzeixCB
```

## Current files
- `CrouzeixCB.lean` — numerical range, closed disk, matrix-valued calculus,
  open cb statements (`sorry`, not `True` stubs). Includes
  `cb_for_perturbed_nilpotent` for `S_n + εE`.
- `NilpotentShift.lean` — 2×2 nilpotent: `S² = 0`, `W(S) ⊆ {|z| ≤ 1/2}`,
  `‖S‖ = 1`, scalar ratio of `p(z) = z` is exactly 2.
- `NilpotentShift3.lean` — `W(S₃) = disk(0, cos(π/4))`. The inclusion
  `W ⊆ disk` is proved; the reverse uses named `sorry`s (Toeplitz–Hausdorff
  convexity and a phase-rotation identity).

## What is proved vs open
Proved (elementary, no dilation theory):
- `NilpotentShift.jordanNilpotent2_sq`
- `NilpotentShift.abs_rayleigh_le_half`
- `NilpotentShift.eNorm_mulVec_le` + attaining vector `e1`
- `NilpotentShift.scalar_monomial_ratio_eq_two`
- `NilpotentShift3.numericalRange_subset_closedDisk`
- `NilpotentShift3.abs_rayleigh_le_cos_pi_div_four`

Open / `sorry` (do **not** treat as theorems):
- `completely_bounded_crouzeix_conjecture`
- `disk_is_complete_two_spectral`
- `cb_for_nilpotent_shifts` (reduces to the disk theorem)
- `cb_for_perturbed_nilpotent` — first open non-disk special class
- `cb_for_weighted_shifts`
- reverse inclusion in `NilpotentShift3.closedDisk_subset_numericalRange`
  (named missing steps)

The unweighted Jordan nilpotent has disk numerical range, so its cb=2
statement is classical once the disk theorem is formalized. Perturbed
nilpotents and weighted shifts are the first classes whose numerical
ranges are not disks.
