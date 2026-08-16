# Imported snapshots — Hygra

**Status:** first static export, 2026-08-16.

## Origin
- Source repository: local `hygra` (read-only).
- Commit: `9e71ce9`.
- Intake: `examples/operator-intake.synthetic.json` (already labelled “not a real site”).
- Exporter: `numerical/export_cem_snapshots.py`.

## Matrices
See `manifest.json`. Four Jacobians, n ≤ 3:

| file | kind | n | what |
|------|------|---|------|
| `envelope-dqdt-3room.json` | jacobian | 3 | ∂Q_env/∂T_in for flower / veg / dry |
| `flower-hvacd-jacobian.json` | jacobian | 2 | (qNetSens, qLat) vs (T_in, P_light), primary ET |
| `veg-hvacd-jacobian.json` | jacobian | 2 | same family on veg-01 (nearly-commuting pair) |
| `flower-hvacd-jacobian-alt-latent.json` | jacobian | 2 | alternate lighting-power latent fraction |

## Anonymization
Synthetic demo rooms only (`flower-01`, `veg-01`, `dry-01`). No facility name, address, or customer identifiers.

## How to regenerate
```bash
python numerical/export_cem_snapshots.py
```
