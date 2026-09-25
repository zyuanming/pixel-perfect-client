---
name: visual-reconstruction
description: Convert an exact screenshot, ImageGen result, mockup, or Figma frame into a measurable design spec and asset plan before writing production UI code.
---

# Visual Reconstruction

Use after client-bootstrap when the task has an exact visual target.

## Input gate

Do not proceed without a resolvable source visual.

Record:

- source type
- path/node/identifier
- source pixel dimensions
- density if known
- target viewport/device if known
- represented state/theme/content

Never guess which image or variant is the target.

## Primary output

Write:

`.pixel-perfect/spec/design-spec.json`

Validate it against:

`schemas/design-spec.schema.json`

The spec is the machine-readable contract between design analysis, optional Figma editing, implementation, and QA.

## Reconstruction workflow

### 1. Normalize the source

Before measuring, identify:

- app-owned content bounds
- device frame/browser chrome that should be excluded
- source density
- crop
- orientation
- safe-area/system-region assumptions

Do not measure fake outer device chrome as application layout.

### 2. Decompose the screen

Build a hierarchy of regions and elements.

Typical categories:

- native/system surface
- container/section
- editable text
- standard icon
- custom vector/raster asset
- decorative artwork
- interactive control
- repeated component
- procedural visual

Give every important element a stable semantic ID.

### 3. Measure geometry

Capture, when visible:

- x/y
- width/height
- margins
- padding
- gaps
- alignment
- radii
- separator thickness
- baseline relationships
- z-order/overlap
- content mode/crop

Do not rely on "looks about right" when the image can be measured.

### 4. Reconstruct typography

For each text style, record:

- visible string
- likely font family or closest available family
- size
- weight
- line height
- letter spacing
- alignment
- wrapping/truncation
- text color
- confidence

Important: generated images may contain glyphs that do not correspond exactly to any real font. Mark this uncertainty instead of claiming an exact font.

Prefer real, legally usable fonts. On Apple platforms, consider system fonts first when the reference is compatible; otherwise select an explicit bundled/free font when licensing allows.

### 5. Reconstruct color and effects

Record:

- solid colors
- semantic role
- opacity
- gradients when real
- border/stroke
- shadow/elevation
- blur/material
- blend/mask behavior

Sample/infer colors from the image, but mark low-confidence values as estimates.

### 6. Build an asset catalog

For every non-trivial visible asset, classify:

- supplied asset
- platform/system icon
- product icon
- raster illustration/photo
- vector artwork
- generated asset
- procedural visual
- 3D asset

Do not replace artwork with approximate code drawing merely because code drawing is possible.

Keep editable UI text out of raster assets unless the text is intrinsically part of the artwork.

### 7. Choose a renderer strategy

Record the lowest-complexity faithful implementation class:

- native layout/control
- image asset
- vector asset
- Core Graphics / Canvas
- Core Image / filters
- shader / Metal
- real-time 3D
- offline 3D-authored asset

Use advanced rendering only where needed.

### 8. Record ambiguity

Every inferred value should have a confidence level where useful:

- high
- medium
- low

Examples of low-confidence items:

- exact font family from raster text
- blur radius
- hidden padding behind artwork
- original vector path
- generated-image glyph details

Ambiguity should guide QA; it should not be silently hidden.

## Figma synchronization

Figma is optional.

When used, reconstruct from the design spec rather than using Figma as the only data source.

Prefer:

- real text layers
- components
- Auto Layout/constraints
- product tokens
- official platform resources
- separate artwork assets

Do not bake the entire screenshot into a single background image and call the reconstruction complete.

## Exit criteria

Before implementation begins:

- source target is exact
- hierarchy exists
- major geometry is measured
- typography is represented
- asset catalog exists
- renderer strategy exists
- unresolved ambiguity is recorded
- design spec validates
