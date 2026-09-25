---
name: client-implementation
description: Implement a reconstructed design spec in the project's real client UI stack while preserving native platform behavior and isolating artwork from application layout.
---

# Client Implementation

Use after visual-reconstruction, or directly for non-reference tasks that already have an equivalent structured design source.

## Inputs

Required:

- client-bootstrap result
- `.pixel-perfect/spec/design-spec.json` or equivalent exact design source
- project source tree

For screenshot-driven work, do not implement from memory after seeing the reference once. Keep the reference/spec accessible throughout the build.

## General rules

- Preserve the existing UI architecture when practical.
- Reuse production tokens/components before creating new ones.
- Prefer platform-native controls for system behavior.
- Separate layout from decorative assets.
- Make the target state deterministic so validation can capture it repeatedly.
- Do not optimize for one screenshot by breaking interaction, accessibility, text sizing policy, or basic responsiveness unless the user explicitly requests a static mock.
- Do not introduce an advanced renderer where a simpler one is faithful.

## Renderer decision

Use the simplest adequate layer.

### Apple platforms

Typical order:

1. SwiftUI / UIKit / AppKit layout and controls
2. Core Animation
3. Core Graphics or SwiftUI Canvas
4. Core Image
5. Metal/shader
6. RealityKit/SceneKit when true interactive 3D is required
7. offline Blender/3D asset authoring when runtime 3D is unnecessary

Blender is an asset-production tool, not a replacement for ordinary application UI.

A game engine should not be the default solution for calendar, settings, feed, editor chrome, forms, or other normal client screens.

### Android

Typical order:

1. Compose / Android Views
2. Canvas/vector/raster assets
3. RenderEffect/shaders where appropriate
4. OpenGL/Vulkan only when the effect truly needs it

### Cross-platform

Honor the existing framework and use platform-specific escape hatches only for fidelity/performance requirements that the shared layer cannot satisfy cleanly.

## Native/system UI

When the source contains a system control or behavior, prefer the actual platform component/API.

Do not manually redraw platform UI solely to make a static screenshot look closer if the real component can produce the intended product behavior.

Device bezel, status bar, home indicator, keyboard, and similar runtime-owned surfaces should be treated according to the actual runtime/capture strategy rather than copied from a mockup as arbitrary artwork.

## Artwork

For complex decorative visuals:

- use the supplied original asset when available
- otherwise reconstruct/generate a dedicated asset
- preserve crop, scale, transparency, and focal point
- avoid approximating the artwork with dozens of ad hoc code shapes

Examples that often belong as assets:

- ink-wash landscapes
- textured moons/planets
- editorial illustration
- photo-real objects
- ornate motifs

Examples that usually stay native/code-rendered:

- text
- separators
- simple rounded surfaces
- standard symbols
- layout backgrounds
- stateful controls

## Typography

Typography drift is often the largest visible mismatch.

Match:

- family/fallback
- optical style
- weight
- size
- line height
- letter spacing
- alignment
- baseline
- wrapping

If the exact reference font is unavailable, choose the closest legally usable option and record the deviation for QA.

## Deterministic capture state

Provide a repeatable way to open the exact target state.

Depending on the project, this may be:

- test launch argument
- debug deep link
- preview/test route
- seeded local data
- snapshot-test host
- dedicated screenshot scheme

Do not require manual tapping through unrelated flows for every visual iteration when a deterministic entry point can be added safely.

## Build gate

Before handing to visual-validation:

- project builds
- target screen launches
- required assets are present
- target content/state is stable
- screenshot capture path is known
- no obvious placeholders remain
