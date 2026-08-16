# Synthetic test matrices

Generated non-normal matrices and simple structured families (nilpotent
shifts, weighted shifts, random triangular, Grcar, Ginibre, mild
non-normal, perturbed nilpotents, CEM-motivated stand-ins) used for
ratio scouting.

Binary `.npy` / `.npz` files are gitignored. The source of truth is
`manifest.json` plus the constructors in `../../numerical/ensembles.py`.

```bash
python ../../numerical/ratio_harness.py   # regenerates this manifest
```

Every random family takes an explicit seed. Structured families
(nilpotent / weighted / Grcar) are deterministic.
