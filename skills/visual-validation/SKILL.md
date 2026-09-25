---
name: visual-validation
description: Compare the exact source visual with a rendered client screenshot, normalize capture conditions, diagnose differences by severity, and iterate until handoff can pass.
---

# Visual Validation

This is a blocking gate for screenshot-driven implementation.

A successful compile, test pass, or app launch is not a visual pass.

## Required evidence

You need both:

- source visual truth
- rendered implementation screenshot

Do not write a fidelity verdict from source code alone.

## 1. Match the comparison state

Before comparing, match:

- viewport/device
- orientation
- crop
- device scale / pixel density
- theme
- dynamic type/text scale
- locale
- content/data
- interaction state
- keyboard/sheet/navigation state
- safe area/runtime-owned system chrome

If they do not represent the same state, fix the capture first.

## 2. Normalize

Record:

- source pixel dimensions
- implementation pixel dimensions
- logical viewport dimensions
- scale/density
- any resize/crop normalization

Prefer equal pixel dimensions for objective diff.

Do not file false findings caused only by browser chrome, device shell, density mismatch, or wrong crop.

## 3. Produce baseline objective evidence

Run:

```bash
python tools/visual-diff/compare.py \
  --reference <source.png> \
  --actual <implementation.png> \
  --out .pixel-perfect/reports
```

Review:

- `report.json`
- `diff.png`
- `heatmap.png`
- `overlay.png`

The numeric score is evidence, not the final judge. Two screens can have a good aggregate score while a critical title, icon, or major region is visibly wrong.

## 4. Inspect fidelity surfaces

Always inspect:

### Geometry
- frame/crop
- section proportions
- alignment
- margins/padding/gaps
- radius
- baseline relationships

### Typography
- font family/fallback
- size/weight
- line height
- letter spacing
- wrapping
- baseline
- glyph differences

### Color/effects
- background/foreground balance
- semantic colors
- opacity
- blur
- shadow
- gradient

### Assets
- subject/art direction
- crop/scale
- transparency halos
- sharpness
- masking
- raster/vector appropriateness

### Content/state
- exact copy
- selected/disabled/active states
- correct data
- correct system surface/state

## 5. Severity

- `P0`: unusable/broken state or severe layout/accessibility failure
- `P1`: major visual mismatch that changes composition, hierarchy, or core identity
- `P2`: noticeable fidelity drift that is clearly actionable
- `P3`: minor polish that need not block handoff

P0/P1/P2 block completion.

## 6. Fix order

Fix the highest-signal cause, not random individual pixels.

Recommended order:

1. state/crop/density mismatch
2. major geometry
3. typography
4. incorrect/missing assets
5. color/effects
6. P3 polish

After a meaningful fix batch:

- rebuild
- recapture
- rerun comparison
- re-inspect the prior finding

Do not keep editing without fresh evidence.

## 7. QA report

Write:

`.pixel-perfect/reports/design-qa.md`

Required fields:

```markdown
# Design QA

source:
implementation:
viewport:
source pixels:
implementation pixels:
density normalization:
state:

## Findings
...

## Iteration history
...

## Residual differences
...

final result: passed
```

If capture/comparison is blocked:

`final result: blocked`

and name the blocker.

## Pass rule

Pass when:

- there are no actionable P0/P1/P2 findings
- source and implementation state match
- required evidence exists
- remaining deviations are explicitly classified

P3 items may remain as follow-up polish.

Do not use a single similarity percentage as the only pass condition.
