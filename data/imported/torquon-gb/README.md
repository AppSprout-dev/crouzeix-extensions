# Imported snapshots — Torquon-GB

**Status:** first static export, 2026-08-16.

## Origin
- Source repository: local `Torquon-GB` (read-only).
- Commit: `2be4790`.
- Exporter: `numerical/export_cem_snapshots.py` (rebuilds the published operators; does not write into Torquon-GB).

## Matrices
See `manifest.json`. Four operators, all n ≤ 16:

| file | kind | n | what |
|------|------|---|------|
| `q4-element-k.json` | stiffness | 8 | Sigmund Q4 `TopologyField.ElementK` (ν=0.3) |
| `mbb-2x2-free-stiffness.json` | stiffness | 14 | solid MBB 2×2, free DOFs after published supports |
| `endplate-3x2-corner-grounded.json` | stiffness | 16 | solid plate, 4-corner ground (`EndPlateLoadCase`) |
| `vdi-flange-axial-spring.json` | stiffness | 2 | VDI-2230 flange spring `k=E·A/L` |

## Anonymization
No part numbers, customer names, or absolute paths. Geometry is the published default flange / downscaled plate, not a customer housing.

## How to regenerate
```bash
python numerical/export_cem_snapshots.py
```
