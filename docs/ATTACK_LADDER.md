# Attack ladder (internal)

Process memo only: stage gates for this isolated operator-theory repo.
Unlock the next floor only when the prior one holds. Do not skip floors.

For the layered campaign (scouting, special classes, dilation, joint ranges),
see `docs/attack-plan.md`. For the open analytic questions, see
`docs/open-problems.md`. This file does not replace either.

## North star

Isolated research on completely-bounded Crouzeix / joint spectral-set
extensions. Scalar Crouzeix (sharp constant 2) is settled elsewhere
(Jin; Lorist–Schwenninger). CB + multi-operator remain open.

## Ladder

Unlock the next stage only when the prior floor holds.

| Stage | Floor | What exists | Still open |
|---|---|---|---|
| **0** | Numerical scout baselines | Johnson scout; ratios ≈2.0000 in `experiments/2026-08-16-baseline/` | Keep re-running when ensembles change |
| **1** | Lean toys / nilpotent-shift lemmas | `lean/NilpotentShift*.lean`, mathlib | Strengthen / more lemmas |
| **2** | Completely-bounded (cb) constant attacks | `lean/CrouzeixCB.lean`, `lean/CrouzeixCOR.lean` stubs/attacks | Prove or refute cb analogue with constant 2 |
| **3** | Multi-operator / joint spectral-set | `docs/open-problems.md` | Joint extensions |
| **4** | CEM handoff (read-only) | Documented settled constants for Phenara / Hygra / Torquon / Unsga3 consumers | Only after a stage is settled + documented; no PRs into CEM repos |

## Isolation rules

- This repository is independent of the AppSprout CEM repositories. Agents
  here must not open PRs, modify files, or create issues in any CEM tree.
- CEM agents may read settled theorems, Lean lemmas, and documented
  constants from here. No automatic dependency is created.
- No Navier–Stokes or Millennium framing belongs in this workstream.

## Non-goals

No 10k-agent theater, no product GTM, no coupling into Unsga3 / Phenara
builds.
