# pixel-perfect-client

An open-source, agent-oriented workflow for turning visual references into production client UI with a measurable **render → screenshot → compare → fix** loop.

> Status: **alpha / v0.1 bootstrap**

## Why

Image-to-code often fails for native apps because a screenshot is only the final raster result. It does not contain the original layout constraints, typography tokens, asset boundaries, component hierarchy, or implementation decisions.

This project adds the missing engineering layer:

```text
reference image / Figma
        ↓
visual reconstruction
        ↓
design-spec.json
        ↓
native implementation
        ↓
build + simulator/device
        ↓
screenshot
        ↓
visual diff + QA
        ↓
fix and repeat
```

Figma is supported, but **Figma is optional**. The machine-readable design spec and rendered evidence are the durable interface between design and code.

## Goals

- Make screenshot-driven UI implementation measurable instead of subjective.
- Support native client stacks first: iOS/iPadOS/macOS, then Android and cross-platform clients.
- Prefer platform-native controls and official platform resources over hand-drawn imitations.
- Keep decorative raster/vector assets separate from layout and editable UI text.
- Work with free/local tooling where possible.
- Make visual QA a blocking handoff gate for reference-driven work.
- Keep the workflow agent-agnostic: Skills + CLI first, MCP later.

## Repository layout

```text
SKILL.md                         Orchestrator
skills/
  client-bootstrap/              Product/platform/Figma/bootstrap safety
  visual-reconstruction/         Reference → design spec + asset plan
  client-implementation/         Design spec → production client code
  visual-validation/             Render → screenshot → compare → iterate
schemas/
  design-spec.schema.json        Machine-readable design contract
tools/
  visual-diff/                   Local visual comparison CLI
  screenshot/                    Platform screenshot helpers
docs/
examples/
```

## Core principle

**Never declare screenshot-driven implementation complete from source code alone.**

For a reference-driven task, completion requires rendered evidence from the target runtime and a comparison against the source visual.

## Figma philosophy

Figma is a human-friendly editor and review surface, not the only source of truth.

A recommended flow is:

```text
reference
   ↓
design-spec.json
   ├──→ Figma (optional editing/review)
   └──→ production code
```

The bundled bootstrap skill includes a Starter-compatible profile and supports a local Desktop Bridge / plugin workflow when available.

## Visual diff quick start

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r tools/visual-diff/requirements.txt

python tools/visual-diff/compare.py \
  --reference reference.png \
  --actual actual.png \
  --out .pixel-perfect/report
```

The command writes:

- `report.json`
- `diff.png`
- `heatmap.png`
- `overlay.png`

## Roadmap

- [x] Skill architecture
- [x] Design spec schema
- [x] Local screenshot helpers
- [x] Baseline visual-diff CLI
- [ ] Automatic reference decomposition
- [ ] Better typography diagnosis
- [ ] Geometry-aware alignment
- [ ] Native iOS accessibility/view-hierarchy inspection
- [ ] Android hierarchy inspection
- [ ] Region-level fix suggestions
- [ ] Optional Figma synchronization
- [ ] Visual MCP wrapper

## License

MIT
