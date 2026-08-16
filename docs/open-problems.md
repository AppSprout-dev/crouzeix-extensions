# Open problems

1. **Completely-bounded Crouzeix with constant 2**  
   Does \(\|F(A)\| \le 2 \sup_{z \in W(A)} \|F(z)\|\) hold for all matrix-valued analytic \(F\)?  
   Known: complete \((1+\sqrt{2})\)-spectral set (Crouzeix–Palencia / COR). Sharp cb=2 known for some special classes (disks; Choi cyclic weighted shifts). No finite pair with shipped ratio \(> 2\) is known, and none should be used as a refutation gate.

### Why the 2026 scalar proofs do not lift (LS Lemma 1)

Lorist–Schwenninger (arXiv:2608.03841, Remark 4(5)) and Jin settle only the *scalar* theorem. In the scalar proof, \(E_n = \theta(\alpha(f^n))\) commutes with \(T = \theta(f)\) because \(\alpha(f^n)\,f = f\,\alpha(f^n)\) inside the commutative uniform algebra \(\mathcal{A}\). After amplification,
\(E_n^{(k)} = \theta^{(k)}(\alpha^{(k)}(F^n))\) versus \(T = \theta^{(k)}(F)\) would need
\(\alpha^{(k)}(F^n)F = F\,\alpha^{(k)}(F^n)\) in \(M_k(\mathcal{A})\), which fails.

The commutativity-free target is Clouâtre–Ostermann–Ransford Conjecture 1.1(ii)
(J. Operator Theory 90, 2023): if \(\alpha\) is a unital antilinear *complete*
contraction, \(\theta\) a unital homomorphism, and \(\Lambda := \theta + \theta\circ\alpha(\cdot)^*\)
satisfies \(\|\Lambda\|_{\mathrm{cb}}\le 2\), then \(\|\theta\|_{\mathrm{cb}}\le 2\).
Known without commutativity: \(\|\theta\|_{\mathrm{cb}}\le 1+\sqrt{2}\) (COR Prop. 6.2;
Lean: `COR.cor_quartic_bound`). The constant-2 statement is that conjecture,
not a missing special-class lemma.

2. **Multi-operator / joint spectral sets**  
   Find a set \(K \subset \mathbb{C}^k\) built from joint numerical ranges such that a joint functional calculus satisfies a uniform bound of controlled constant.

3. **Dimension-dependent or non-normality-dependent improvements**  
   Even short of the universal cb=2, any improvement over \(1+\sqrt{2}\) that depends on dimension or self-commutator size is valuable for CEM operators.

4. **Extremal examples for the cb ratio**  
   Systematic search for matrices (or amplifications) that force the ratio close to the best possible constant.

## Status notes (2026-08-16)

- Unweighted nilpotent Jordan blocks are *not* an open cb class: `W(S_n)`
  is a disk of radius `cos(π/(n+1))`, and a disk is a complete 2-spectral
  set. The n=2 scalar sharpness `‖S‖/w(S) = 2` is formalized in
  `lean/NilpotentShift.lean`. The remaining Lean work for this family is
  the disk theorem itself.
- First open special classes in this repository:
  1. controlled perturbations `S_n + εE` (W not a disk);
  2. *general* (non-cyclic) weighted shifts;
  3. general 3×3 nilpotents that are not a single Jordan block.
- Choi’s *cyclic* family `M(α) = P_d diag(α)` is *not* open: Crouzeix–Greenbaum
  (arXiv:2508.12768) prove it is a complete 2-spectral set. The disk example
  `M(2sin φ, 2cos φ, 0)` has `ψ = 2 max(sin φ, cos φ, sin 2φ) ∈ [√3, 2]` and
  is a regression gate in `numerical/test_harness.py`.
- Johnson `W(A)` (finite supporting-line sample) can under-estimate the
  boundary and inflate a ratio. A probe `> 2+1e-3` outside a provably-≤2
  family is an alert (possible sampler bug), not a claimed counterexample.
- Empirical cb probes on random low-degree amplifications have not yet
  produced a ratio near 2 except for the trivial amplification
  `F(z) = z I_k` on `S_2`. The 2026-08-16 large campaign (`k ∈ {8,12}`,
  `degree ∈ {3,4}`, 10 random probes) had max ratio 1.1017. Structured
  near-extremal `F` is the next numerical search.
