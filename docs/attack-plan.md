# Attack plan for completely-bounded and multi-operator extensions

## Goals
1. Completely-bounded Crouzeix statement with constant 2 (or the best attainable universal constant).
2. Usable multi-operator / joint spectral-set bounds, especially for small tuples or nearly-commuting families that appear in multi-physics CEMs.

## Layered approach

### 1. Numerical scouting (immediate)
- Export or generate representative matrices from CEM operators (stiffness, transfer, structural, multi-zone Jacobians).
- Amplify to modest matrix-valued polynomials and compute empirical cb-ratios.
- Parallel random non-normal ensembles for baseline.
- Log observed ratios versus dimension, self-commutator size, and numerical-range geometry.

### 2. Special-class campaign
Prove the sharp cb statement first for families that already possess scalar proofs and that model CEM operators:
- nilpotent shifts and controlled perturbations,
- weighted shifts (transport-like),
- low-dimensional Jordan-like blocks,
- matrices whose numerical range is an ellipse or simple polygon.

Each settled class becomes a verified Lean lemma.

### 3. Abstract dilation / completely-positive route
Recast via unital completely-bounded maps, Stinespring dilations, and matrix-valued positive-real completions. The scalar proofs use double-layer potentials and 2-dilations; the missing piece is a completely-positive counterpart that survives amplification.

### 4. Joint numerical ranges
Begin with commuting or nearly-commuting tuples (common in multi-physics settings). Seek constants that depend at most on the number of operators or on a joint non-normality measure.

### 5. Formalization + AI-assisted search
- Lean 4 + mathlib as the verification target.
- LLM agents propose sketches and counter-examples; Lean checks; human/secondary review confirms fidelity to the analytic claim.
- Maintain a living set of open goals and partial results.

## Feedback to CEMs
Any partial result (cb constant for a concrete class, or a joint bound under a commutator-size hypothesis) is documented here and may be cited by CEM agents. No automatic dependency is created.

## Progress log

### 2026-08-16
- Numerical harness now uses Johnson’s supporting-line estimate of `W(A)`.
  The original Monte-Carlo n=8 ratio ~6.5 was an underestimate of
  `max |p|` and is not a Crouzeix violation.
- First scout (`experiments/2026-08-16-baseline/`): 242 scalar Johnson
  ratios, max 2.0000; 17 cb probes, max 2.0000. No record above
  `2 + 10^{-3}`.
- Special-class clarification: unweighted Jordan nilpotents have *disk*
  numerical range, so cb=2 is classical (Okubo–Ando / Berger). Lean has
  the n=2 scalar sharpness (`lean/NilpotentShift.lean`). The first
  genuinely open special classes are **perturbed nilpotents** and
  **weighted shifts**.
- Imported-data layout ready; no live CEM pull.

### 2026-08-16 (pin / n=3 / large cb)
- Mathlib pinned in `lean/` (`v4.34.0-rc1`, rev `274ed6d67d9b226c557813b9ce437574cccdce11`).
- `W(S₃) = disk(0, cos(π/4))` stated with both inclusions; `W ⊆ disk` proved.
- Open theorem `cb_for_perturbed_nilpotent` for `S_n + εE`.
- Large cb campaign: max random `k≥8`, `deg≥3` ratio 1.1017; none above 2.
- First static CEM snapshots accepted: Torquon-GB@`2be4790` (4 stiffness) and Hygra@`9e71ce9` (4 Jacobians). No writes into those repos.

### 2026-08-16 (COR route)
- Complete constant 2 stays open. No `(A, F)` with shipped ratio `> 2+1e-3`
  is a legitimate refutation gate (Johnson can inflate ratios).
- Regression gates: exact-2 on `S₂` + `z I_k`; ≤2 on `S_n` (disk) and
  Choi `M(2sin φ, 2cos φ, 0)` (Crouzeix–Greenbaum, complete 2-spectral).
- Lean milestone: `COR.cor_quartic_bound` (`κ ≤ 1+√2` from the COR quartic).
  Next complete step is constructing Φ and α; then COR 1.1(ii) for constant 2.
- LS Lemma 1 fails after amplification (non-commuting `α(Fⁿ)F` vs `F α(Fⁿ)`).
