# visual-diff

Small local baseline comparator used by the `visual-validation` skill.

## Install

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r tools/visual-diff/requirements.txt
```

## Compare

```bash
python tools/visual-diff/compare.py \
  --reference reference.png \
  --actual actual.png \
  --out .pixel-perfect/reports
```

By default, image dimensions must match.

If you intentionally need a temporary density-normalized comparison:

```bash
python tools/visual-diff/compare.py \
  --reference reference.png \
  --actual actual@2x.png \
  --normalize resize-actual \
  --out .pixel-perfect/reports
```

Prefer capturing equal-size images instead of relying on resizing.

## Outputs

- `report.json`
- `diff.png`
- `heatmap.png`
- `overlay.png`

The CLI exit code is:

- `0`: baseline thresholds passed
- `1`: baseline thresholds blocked
- `2`: invalid comparison, such as strict dimension mismatch

A baseline pass does **not** replace visual QA.
