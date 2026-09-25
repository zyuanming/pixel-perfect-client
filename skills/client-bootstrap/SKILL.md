---
name: client-bootstrap
description: Discover the real client product, platform, UI framework, design-system context, optional Figma target, and safe tool routing before design or implementation work.
---

# Client Bootstrap

Run before reference reconstruction or client UI implementation.

## Objective

Resolve the real identity chain:

```text
Repository
→ Product
→ Platform
→ UI framework
→ Design system
→ Runtime target
→ Optional canonical Figma
```

Do not mechanically assume:

- one Git repository = one product
- an iOS directory means the product is iOS-only
- Swift files mean SwiftUI
- an extension deserves its own design file
- the currently open Figma document is the right target

## Repository and product discovery

Inspect the minimum evidence needed:

- repository root and directory name
- README / AGENTS.md
- build metadata
- source tree
- targets/schemes/modules
- bundle IDs / application IDs
- project/workspace/package files
- existing design-system code
- existing design bindings

Classify the repository as one of:

- independent product
- extension/sub-product
- shared module/design system
- cross-platform product

If ownership is ambiguous and a write could affect another product, stop the write and report `PRODUCT_OWNERSHIP_AMBIGUOUS`.

## Detect the real UI stack

Examples:

Apple:
- SwiftUI
- UIKit
- AppKit
- mixed SwiftUI/UIKit
- mixed SwiftUI/AppKit

Android:
- Jetpack Compose
- Android Views
- mixed

Cross-platform:
- Flutter
- React Native
- Kotlin Multiplatform
- Compose Multiplatform

Web/Desktop:
- detect from project evidence

Preserve the existing stack unless the user explicitly asks for migration or the current stack cannot satisfy the target.

## Existing code is evidence

Before inventing a design system, inspect existing:

- colors/tokens
- typography
- spacing/radius
- reusable components
- navigation patterns
- asset catalogs
- platform wrappers
- themes
- existing screens

Aim for:

```text
Product design language
↕
Design spec / Figma
↕
Client design system
↕
Production UI
```

## Official platform resources first

When a platform already provides an official control, icon, system surface, device/runtime behavior, or documented typography convention, prefer that over a custom imitation.

Examples on Apple platforms include native navigation, tab bars, sheets, alerts, pickers, keyboard behavior, home indicator/device behavior, and SF Symbols where suitable.

If an official device bezel is unavailable, show a bare screen rather than a fake hardware shell.

Do not confuse "official platform resource" with any particular Figma connector.

## Optional Figma profile

Figma is optional for this project.

When the environment is configured to use a local Figma Console / Desktop Bridge workflow, prefer that configured route for Figma Design reads/writes.

Do not silently switch to another connector, another product, or another Figma document when the configured route fails.

### Target safety

Before any Figma write:

1. verify product identity
2. verify canonical file identity/key when available
3. verify bridge/session
4. explicitly target the canonical file
5. lock/confirm the target when tooling supports it
6. perform the write
7. re-read/verify the result

Never infer the write target from:

- active tab
- current selection
- frontmost document
- last connected file
- last plugin response

Never fall back to another product.

### Starter-compatible default profile

When the repository/user selects the Figma Starter compatibility profile, default to:

- at most 3 pages
- one variable mode per collection
- sections/frames instead of extra pages
- local components/variables
- no dependency on paid cross-file libraries

Recommended pages:

```text
01 — Design System
02 — Product
03 — Playground
```

Recommended organization under Design System:

```text
Foundations
Variables
Colors
Typography
Spacing
Radius
Elevation
Icons
Platform / Official
Platform / Custom
Base Components
Product Components
```

Treat these as a compatibility profile, not an excuse to invent capabilities the connected account does not have.

## Multi-agent safety

Assume multiple agents/products can be active simultaneously.

A valid target identity is stronger in this order:

```text
stable file/product identifier
> canonical URL
> exact canonical name
> product identity
> repository name
> active UI state
```

If a destructive or cross-product action is ambiguous, stop.

## Bootstrap output

Record or report:

```text
Repository:
Product:
Product type:
Parent product:
Platform:
UI framework:
Application / bundle ID:
Runtime target:
Design system evidence:
Canonical Figma (optional):
Figma route (optional):
Starter profile active: yes/no
Blocking ambiguity: none / details
```

Then hand off to visual-reconstruction or client-implementation.
