# Imported snapshots — Hygra

**Status:** layout only. No matrices yet.

## Expected contents
3–5 small multi-zone environmental or resource Jacobians, dimension ≤ 32.
Nearly-commuting families are preferred (early joint-spectral-set tests).

## When a snapshot arrives
1. Follow `../SCHEMA.md`.
2. Record origin, date, and any anonymization in this README.
3. Do **not** pull live from the Hygra repository and do **not**
   open PRs or issues there. Static files only.

## Why this family
Multi-zone Jacobians are the realistic nearly-commuting tuples for the
joint numerical-range campaign. Scalar Crouzeix already applies
operator-by-operator; a joint bound is the CEM-facing goal.
