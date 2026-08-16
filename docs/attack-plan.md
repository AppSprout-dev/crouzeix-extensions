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
