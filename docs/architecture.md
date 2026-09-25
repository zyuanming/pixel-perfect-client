# Architecture

`pixel-perfect-client` separates design reconstruction from implementation and implementation from validation.

## The problem

A screenshot contains final pixels but not the original:

- constraints
- semantic hierarchy
- component model
- font metadata
- asset boundaries
- native/system ownership
- interaction behavior

Asking an agent to jump directly from image to code forces it to guess all of those at once.

## Pipeline

```text
               ┌────────────────────┐
               │ visual reference   │
               │ image/Figma/golden │
               └─────────┬──────────┘
                         │
                         ▼
              ┌──────────────────────┐
              │ visual reconstruction│
              └─────────┬────────────┘
                        │
                        ▼
                design-spec.json
                  │             │
                  │             └────→ Figma (optional)
                  ▼
           client implementation
                  │
                  ▼
             target runtime
                  │
                  ▼
               capture
                  │
                  ▼
              visual diff
                  │
                  ▼
              design QA
                  │
             ┌────┴────┐
             │         │
          fix loop   handoff
```

## Why Figma is optional

Figma is excellent for human editing and review, but the agent should not require a paid design-file feature to preserve measurements or run runtime validation.

The durable machine-facing contract is the design spec plus visual evidence.

This makes the workflow useful when:

- the designer only has a screenshot
- the project uses Figma Starter
- Figma is temporarily unavailable
- the implementation is native and runtime truth matters more than a design-file representation

## Skill boundaries

### client-bootstrap

Answers: *What product and stack am I actually modifying, and what is the safe design target?*

### visual-reconstruction

Answers: *What measurable design is represented by this reference?*

### client-implementation

Answers: *How should this design be implemented in the real client stack?*

### visual-validation

Answers: *What still differs after the real runtime renders it?*

## Why Skills + CLI before MCP

The high-value capability is the executable behavior:

- capture
- compare
- measure
- report
- iterate

MCP is an interface layer around that capability.

The project therefore starts with portable Skills and local CLI tools. Once tool contracts stabilize, an MCP server can expose them without changing the underlying workflow.

## Evidence hierarchy

For visual fidelity work:

```text
rendered runtime evidence
> production source-code intent
> design-file interpretation
> agent memory
```

For product identity and safe writes:

```text
stable product/file identifier
> canonical binding
> repository evidence
> active UI state
```

## Completion semantics

"Build succeeded" means the code compiled.

"Visual baseline passed" means numeric image thresholds passed.

"Design QA passed" means the normalized source and implementation have no remaining actionable P0/P1/P2 differences.

Only the last state is a valid handoff for screenshot-driven fidelity work.
