# Snapshot schema for imported CEM matrices

Static files only. No live coupling to Torquon-GB, Hygra, or any other
CEM repository.

## Layout
```
data/imported/<cem-name>/
  README.md          # origin, date, anonymization, license/permission
  manifest.json      # list of matrices in this snapshot
  <id>.json          # one matrix per file (preferred for n ≤ 32)
```

## Matrix file (`<id>.json`)
```json
{
  "id": "torquon-gb/stage2-stiffness-001",
  "cem": "torquon-gb",
  "kind": "stiffness",
  "n": 8,
  "dtype": "complex128",
  "real": [[0.0, 1.2], [0.0, 0.3]],
  "imag": [[0.0, 0.0], [0.0, 0.0]],
  "units": "N/m",
  "notes": "optional free text; no proprietary identifiers"
}
```

- `real` / `imag` are dense row-major lists of lists, shape `n × n`.
- Prefer dimension ≤ 32 for the first export.
- Anonymize part numbers, customer names, and absolute file paths.
- Do not commit files larger than a few megabytes without git-lfs.

## Manifest (`manifest.json`)
```json
{
  "cem": "torquon-gb",
  "exported": "YYYY-MM-DD",
  "matrices": ["stage2-stiffness-001.json"]
}
```
