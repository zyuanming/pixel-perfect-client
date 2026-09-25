# iOS / iPadOS Implementation Notes

This project does not assume SwiftUI.

Bootstrap should detect whether the application uses:

- UIKit
- SwiftUI
- mixed UIKit + SwiftUI

## Renderer choice

For ordinary application UI, prefer native layout first.

A useful escalation path is:

```text
UIKit / SwiftUI
→ Core Animation
→ Core Graphics / SwiftUI Canvas
→ Core Image
→ Metal / shader
→ RealityKit / SceneKit for true interactive 3D
→ offline Blender for authored assets
```

The existence of a photorealistic moon, illustration, or textured object in a mockup does not imply the whole screen needs Metal or a game engine.

## Example: decorative moon

If the moon is static:

- use a dedicated image asset
- preserve transparency/crop
- render with normal native layout

If the moon phase changes procedurally:

- consider masking/Canvas/Core Graphics/Core Image

If the user can rotate a true 3D moon:

- consider RealityKit/SceneKit/Metal depending on requirements

Blender may still be useful to author or bake the texture/normal map, but it is not the screen layout engine.

## Example: ink landscape

A detailed ink-wash footer is normally a raster/vector artwork asset.

Do not rebuild it from many SwiftUI Shapes just to keep everything "code-native."

## Capture

For an already booted Simulator:

```bash
tools/screenshot/ios-sim.sh
```

Or:

```bash
xcrun simctl io booted screenshot .pixel-perfect/captures/ios-simulator.png
```

Use a deterministic launch state whenever possible.

## Snapshot tests

Snapshot testing can complement full-app capture, especially for isolated components or view controllers.

Snapshot tests are useful regression evidence, but when the user's target is a full reference screen, also validate the actual full rendered state and its runtime-owned system surfaces.
