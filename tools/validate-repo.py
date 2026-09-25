#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

REQUIRED = [
    "README.md",
    "SKILL.md",
    "skills/client-bootstrap/SKILL.md",
    "skills/visual-reconstruction/SKILL.md",
    "skills/client-implementation/SKILL.md",
    "skills/visual-validation/SKILL.md",
    "schemas/design-spec.schema.json",
    "examples/calendar/design-spec.json",
    "tools/visual-diff/compare.py",
]


def fail(message: str) -> None:
    raise SystemExit(f"validation failed: {message}")


for relative in REQUIRED:
    path = ROOT / relative
    if not path.exists():
        fail(f"missing required file: {relative}")

for relative in [
    "SKILL.md",
    "skills/client-bootstrap/SKILL.md",
    "skills/visual-reconstruction/SKILL.md",
    "skills/client-implementation/SKILL.md",
    "skills/visual-validation/SKILL.md",
]:
    text = (ROOT / relative).read_text(encoding="utf-8")
    if not text.startswith("---\n"):
        fail(f"{relative} is missing YAML frontmatter")
    if "\nname:" not in text or "\ndescription:" not in text:
        fail(f"{relative} frontmatter requires name and description")

schema = json.loads((ROOT / "schemas/design-spec.schema.json").read_text(encoding="utf-8"))
example = json.loads((ROOT / "examples/calendar/design-spec.json").read_text(encoding="utf-8"))

if schema.get("title") != "Pixel Perfect Client Design Spec":
    fail("unexpected schema title")

for key in schema.get("required", []):
    if key not in example:
        fail(f"example missing top-level required key: {key}")

print("repository validation passed")
