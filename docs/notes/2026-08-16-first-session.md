# 2026-08-16 — first research session

## Numerical
- Ran the original `numerical/ratio_harness.py`. Baseline scalar ratios on
  random triangular matrices: n=2 → 1.19, n=3 → 1.03, n=4 → 1.31, **n=8 → 6.52**.
- The n=8 figure is a Monte-Carlo artifact: 2000 random Rayleigh samples
  underestimate `max |p|` on `W(A)`, and the monomial `z^{7}` amplifies the
  bias. Johnson supporting-line estimation on the *same* matrices brings
  every legacy ratio back under 2 (n=8 becomes 0.45).
- Extended the harness with structured ensembles (nilpotent / weighted /
  Grcar / Ginibre / mild non-normal / perturbed nilpotent / CEM-motivated
  stiffness and Jacobian stand-ins) and matrix-valued polynomials
  `F(z) = Σ C_j z^j`, `F(A) = Σ C_j ⊗ A^j`.
- Full scout: 242 scalar Johnson records, max ratio **2.0000**; 17 cb
  probes, max ratio **2.0000** (attained only by `F(z) = z I_k` on the
  2×2 nilpotent). Zero records above `2 + 10^{-3}`.
- Log: `experiments/2026-08-16-baseline/`. Manifest:
  `data/synthetic/manifest.json`.

## Lean
- First non-placeholder file: `lean/NilpotentShift.lean`.
- Proved (on paper / ready for mathlib): `S₂² = 0`, `W(S₂) ⊆ disk(1/2)`,
  `‖S₂‖ = 1`, scalar ratio of `z` equals 2.
- Clarified the special-class map: unweighted Jordan nilpotents have
  disk numerical range, so cb=2 is classical (disk theorem). The first
  *open* special classes are perturbed nilpotents and weighted shifts.

## Data
- Prepared `data/imported/torquon-gb/` and `data/imported/hygra/` with
  READMEs and a snapshot schema. No live CEM pull.

## Follow-up (same day)
- Mathlib pinned: `lean/lean-toolchain` (`v4.34.0-rc1`) and
  `lean/lakefile.toml` (mathlib `274ed6d67d9b226c557813b9ce437574cccdce11`).
- `NilpotentShift3.lean`: `W(S₃) ⊆ disk(0, cos(π/4))` proved; reverse
  inclusion stated with named `sorry`s (convexity, phase rotation).
- Open theorem `cb_for_perturbed_nilpotent` for `S_n + εE` (`sorry`, not `True`).
- Large cb campaign (`--large-cb`): 10 probes with `k ≥ 8`, `degree ≥ 3`,
  max random ratio 1.1017; only `z I_8` on `S₂` hits 2.0000. Log:
  `experiments/2026-08-16-cb-large/`. No Torquon-GB / Hygra snapshots arrived.

## Next concrete actions
1. Local `lake build` of `NilpotentShift.lean` (pin is in place; toolchain
   download may still be running in a fresh environment).
2. Close the named `sorry`s in the n=3 reverse inclusion (convexity, phases).
3. Larger / more extremal cb searches (structured F, not only Gaussian coeffs).
4. Accept the first static Torquon-GB / Hygra snapshots when exported.
   **Done:** four Torquon stiffness operators and four Hygra Jacobians
   under `data/imported/`. Scout: `experiments/2026-08-16-imported/`
   (max ratio 1.0002). CEM repos were not modified.

## Blockers
- No Lean/lake toolchain in this environment; lemmas are not machine-checked here.
- No real CEM matrices yet (by design: synthetic first).
