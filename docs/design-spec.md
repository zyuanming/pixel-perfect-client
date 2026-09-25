# Design Spec

The design spec is a small JSON contract that sits between a visual reference and production code.

Schema:

`schemas/design-spec.schema.json`

## Why JSON

The format is:

- easy for agents to produce and revise
- easy to diff in Git
- independent of Figma plans and libraries
- portable across iOS, Android, Flutter, React Native, and desktop clients
- measurable

It is not intended to replace a complete design tool.

## Coordinate space

Every spec declares a canvas coordinate space:

- `source-pixels`
- `logical-points`
- `normalized`

For an initial screenshot reconstruction, `source-pixels` is often easiest because measurements map directly to the visual target.

Implementation should then convert into the runtime's layout model.

## Stable IDs

Use semantic IDs:

```text
screen
calendar.week-strip
calendar.selected-day
hero.primary-date
hero.moon
current-hour.card
footer.ink-landscape
tabbar.calendar
```

Avoid disposable IDs such as `Rectangle 12` or `Frame 198`.

Stable IDs let QA findings refer to the same element across reconstruction, Figma, code, and screenshots.

## Confidence

Raster inference is not always exact.

Use:

- `high`: directly measurable or known
- `medium`: visually inferable with some uncertainty
- `low`: likely approximation

A common low-confidence field is the exact font family in an ImageGen-generated mockup.

## Assets

Classify assets explicitly.

Typical choices:

- `system-icon`
- `product-icon`
- `raster`
- `vector`
- `generated`
- `procedural`
- `3d`

This prevents an agent from replacing a detailed illustration with improvised code shapes.

## Renderer hints

Nodes can carry a renderer hint:

- `native`
- `asset`
- `vector`
- `canvas`
- `core-image`
- `shader`
- `metal`
- `3d`
- `offline-3d`

The hint is a strategy, not a mandate. Existing project architecture still matters.

## Example

See:

`examples/calendar/design-spec.json`

The example demonstrates a calendar screen with real application text plus separate moon and ink-landscape assets.
