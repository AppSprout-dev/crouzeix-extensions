# Open problems

1. **Completely-bounded Crouzeix with constant 2**  
   Does \(\|F(A)\| \le 2 \sup_{z \in W(A)} \|F(z)\|\) hold for all matrix-valued analytic \(F\)?  
   Known: complete \((1+\sqrt{2})\)-spectral set (Crouzeix–Palencia). Sharp cb=2 known for some special classes.

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
  2. weighted shifts;
  3. general 3×3 nilpotents that are not a single Jordan block.
- Empirical cb probes on random low-degree amplifications have not yet
  produced a ratio near 2 except for the trivial amplification
  `F(z) = z I_k` on `S_2`. The 2026-08-16 large campaign (`k ∈ {8,12}`,
  `degree ∈ {3,4}`, 10 random probes) had max ratio 1.1017. Structured
  near-extremal `F` is the next numerical search.
