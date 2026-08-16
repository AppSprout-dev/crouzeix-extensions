# Imported snapshots — Torquon-GB

**Status:** layout only. No matrices yet.

## Expected contents
3–5 small stage operators, dimension ≤ 32, from Torquon-GB test benches:

- stage stiffness matrices under mild tolerance / asymmetric loading;
- optional transfer or damping blocks from the same stage.

## When a snapshot arrives
1. Follow `../SCHEMA.md`.
2. Record origin, date, and any anonymization in this README.
3. Do **not** pull live from the Torquon-GB repository and do **not**
   open PRs or issues there. Static files only.

## Why this family
Gearbox stiffness / transfer / damping blocks are non-normal under
asymmetric loading. They are realistic targets for scalar constant 2
today and for a future cb / joint bound across several stages.
