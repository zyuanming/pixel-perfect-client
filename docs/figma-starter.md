# Figma Starter Compatibility Profile

Figma is optional in `pixel-perfect-client`.

This repository includes a conservative Starter-oriented profile for users who want Figma as an editable review surface without making paid cross-file design-system features a requirement.

## Default profile

When enabled, the workflow assumes:

- at most 3 pages
- one mode per variable collection
- local components and variables
- sections/frames for further organization
- no dependency on paid cross-file libraries

Recommended pages:

```text
01 — Design System
02 — Product
03 — Playground
```

If the connected account exposes different capabilities, the agent should inspect reality rather than inventing unsupported behavior.

## Design System structure

Inside `01 — Design System`:

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

## Official platform resources

"Official platform resources" means resources from the target platform vendor, for example:

- Apple design resources / SF Symbols / platform guidance
- Material Design / Material Symbols
- other platform-owned component resources

It does **not** imply that a particular Figma connector must be used.

## Local Figma route

Some users run a local workflow such as:

```text
agent
→ local Figma console/tool
→ Desktop Bridge/plugin
→ canonical Figma file
```

When a repository is explicitly configured this way:

- honor that route
- do not silently fall back to another connector
- do not switch to another product/file because the target is temporarily disconnected
- restore the configured bridge/session when possible

## Multi-agent safety

Before any Figma write, verify:

1. product
2. canonical file identity
3. connection/session
4. explicit target
5. target lock/confirmation if supported

Never select a write target solely from the currently frontmost Figma tab.

## If Figma is unavailable

Continue with:

- exact source visual
- `design-spec.json`
- local assets
- production code
- runtime screenshot validation

Figma downtime or plan limitations should not prevent visual implementation when the remaining evidence is sufficient.
