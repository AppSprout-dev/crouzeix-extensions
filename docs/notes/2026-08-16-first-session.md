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

## Next concrete actions
1. Local `lake build` of `NilpotentShift.lean` once a mathlib pin exists.
2. Formalize `W(S_n) = disk(0, cos(π/(n+1)))` for `n = 3` (still a disk).
3. Start the perturbed-nilpotent Lean statement (W not a disk).
4. Larger cb amplifications (`k ≥ 8`, degree ≥ 3) on the same synthetic
   families; keep looking for ratios that approach 2 from below.
5. Accept the first static Torquon-GB / Hygra snapshots when exported.

## Blockers
- No Lean/lake toolchain in this environment; lemmas are not machine-checked here.
- No real CEM matrices yet (by design: synthetic first).
