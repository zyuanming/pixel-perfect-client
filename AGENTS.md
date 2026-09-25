# AGENTS.md

## Repository purpose

This repository defines an open-source visual-reconstruction and visual-validation workflow for client applications.

## Design principles

- Skills + CLI first; MCP later.
- Figma is optional.
- Runtime rendering is required evidence for screenshot-driven fidelity.
- Official/native platform UI is preferred over hand-drawn imitations.
- Complex decorative artwork should remain an asset when appropriate.
- Do not turn this project into a framework-specific code generator.
- Keep cross-platform contracts in JSON/Markdown and platform adapters small.

## Required checks before changing core contracts

When modifying `schemas/design-spec.schema.json`:

- keep examples valid
- document incompatible changes
- bump the schema/project version when appropriate

When modifying visual diff behavior:

- preserve machine-readable `report.json`
- preserve non-zero exit code for blocked comparisons
- document threshold changes

When modifying skills:

- keep YAML frontmatter
- keep responsibilities separated
- avoid duplicating the same long policy in every skill

## Figma

The default project philosophy is Figma-optional.

Do not add a hard dependency on a paid Figma plan.

The Starter compatibility profile lives in `docs/figma-starter.md` and `skills/client-bootstrap/SKILL.md`.

## Secrets

Never commit:

- API tokens
- Figma PATs
- passwords
- credentials
- private signing material

## Generated artifacts

Do not commit `.pixel-perfect/captures` or large temporary visual-diff output by default.

Small golden fixtures may be committed when they are deliberate tests.
