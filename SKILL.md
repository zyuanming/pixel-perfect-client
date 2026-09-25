---
name: pixel-perfect-client
description: Reconstruct a client UI from an exact visual reference, implement it in the real client stack, render it in the target runtime, compare screenshots, and iterate until blocking visual differences are resolved.
---

# Pixel Perfect Client

Use this skill when a task starts from a screenshot, ImageGen result, mockup, Figma frame, or other exact visual target and the goal is production client UI.

This is an orchestration skill. It coordinates four focused skills:

1. `skills/client-bootstrap/SKILL.md`
2. `skills/visual-reconstruction/SKILL.md`
3. `skills/client-implementation/SKILL.md`
4. `skills/visual-validation/SKILL.md`

## Non-negotiable rules

- The selected reference is visual truth. Resolve it exactly before implementation.
- Never claim screenshot-driven implementation is complete from source code alone.
- A successful build is not visual verification.
- Figma is optional. Do not make Figma availability a blocker when the reference, design spec, assets, and runtime are sufficient.
- Prefer official platform controls, icons, typography guidance, and device/runtime behavior over hand-drawn imitations.
- Do not approximate complex artwork with code-native shapes when the reference clearly contains a raster/vector asset.
- Keep editable application text as real text. Keep text that is intrinsically part of artwork inside that artwork.
- Use Metal, shaders, 3D engines, or offline 3D tooling only when the visual requirement actually needs them.
- Preserve the project's existing architecture and UI framework unless there is a strong implementation reason to change it.
- For every write to a shared design surface, verify the exact product and target first. Never infer a target from the frontmost tab or last connected document.

## Standard workspace

For reference-driven work, keep generated evidence under:

```text
.pixel-perfect/
  source/
  spec/
    design-spec.json
  assets/
  captures/
  reports/
    design-qa.md
    report.json
    diff.png
    heatmap.png
    overlay.png
```

Do not commit `.pixel-perfect/captures` or large generated artifacts by default unless the repository explicitly wants visual fixtures.

## Required workflow

### 1. Bootstrap

Run the client-bootstrap skill.

Determine:

```text
Repository
→ Product
→ Platform
→ UI framework
→ Existing design system
→ Exact runtime target
→ Optional canonical Figma
```

Do not assume iOS, SwiftUI, or one repository = one product.

### 2. Resolve the source visual

The source must be unambiguous.

Acceptable source truth includes:

- attached screenshot or image
- an explicitly selected ImageGen output
- exact Figma node/frame
- approved mockup
- existing golden screenshot

Record its path/identifier in the design spec.

If the exact source cannot be resolved, stop before implementation.

### 3. Reconstruct

Run the visual-reconstruction skill.

Produce `.pixel-perfect/spec/design-spec.json` that validates against `schemas/design-spec.schema.json`.

At minimum capture:

- reference dimensions and density
- target viewport/device
- regions and hierarchy
- geometry
- typography
- colors/tokens
- assets
- standard/native controls
- interaction state represented by the screenshot
- measurement confidence and unresolved ambiguity

Do not start by writing UI code and then reverse-engineering a spec from the code.

### 4. Implement

Run the client-implementation skill.

Implementation must use the actual application stack and existing project conventions.

The implementation step must leave the project in a buildable/runnable state and expose a deterministic route/state for screenshot capture.

### 5. Render

Build and run the real target runtime.

Examples:

- iOS Simulator
- Android Emulator
- macOS application
- browser/runtime for Flutter or React Native where appropriate

Capture the exact app-owned visual state.

### 6. Validate

Run the visual-validation skill.

Normalize viewport, crop, density, theme, content, and state before judging.

Then compare:

```text
source visual
vs
rendered implementation
```

Use `tools/visual-diff/compare.py` for objective baseline metrics and image artifacts. Use human/agent visual inspection for typography, asset correctness, semantics, and differences the baseline metric cannot explain.

### 7. Iterate

Fix the highest-impact differences first:

1. wrong viewport/crop/state
2. geometry and layout
3. typography
4. assets and imagery
5. colors and effects
6. minor polish

Re-render after each meaningful batch.

Do not keep tuning source code without fresh rendered evidence.

### 8. Handoff gate

A screenshot-driven task may be handed off only when:

- source visual is recorded
- implementation screenshot exists
- dimensions/density/state are recorded
- no actionable P0/P1/P2 visual findings remain
- `.pixel-perfect/reports/design-qa.md` says exactly `final result: passed`

If capture or comparison is impossible, the QA file must say `final result: blocked` and name the blocker.

## Renderer choice

Choose the simplest renderer that can faithfully reproduce the design.

For Apple platforms, default roughly to:

```text
Native UI
→ Core Animation / Core Graphics / SwiftUI Canvas
→ Core Image
→ Metal / shader
→ RealityKit / SceneKit when actual 3D interaction is required
→ offline Blender/3D asset generation when only the asset needs 3D authoring
```

Do not jump to a game engine for ordinary application layout.

## Figma

When Figma is used:

- treat it as an optional editable/review surface
- keep the machine-readable design spec independent
- reuse official platform resources and product components
- honor the client-bootstrap target-safety rules
- use Starter-compatible defaults when that profile is active

Figma synchronization must never replace runtime screenshot verification.
