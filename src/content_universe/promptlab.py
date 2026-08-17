from __future__ import annotations

import json
from dataclasses import dataclass, field, asdict
from typing import Any


@dataclass(slots=True)
class PromptElement:
    kind: str
    text: str | None = None
    description: str | None = None
    raw: dict[str, Any] = field(default_factory=dict)


@dataclass(slots=True)
class PromptDecomposition:
    original: str | None = None
    expanded: Any = None
    high_level_description: str | None = None
    background: str | None = None
    elements: list[PromptElement] = field(default_factory=list)
    is_structured: bool = False

    def to_dict(self) -> dict[str, Any]:
        return {
            **asdict(self),
            "elements": [asdict(e) for e in self.elements],
        }


def _maybe_json(value: Any) -> Any:
    if not isinstance(value, str):
        return value
    text = value.strip()
    if not text.startswith(("{", "[")):
        return value
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        return value


def decompose_prompt(original: str | None, expanded: Any) -> PromptDecomposition:
    parsed = _maybe_json(expanded)
    result = PromptDecomposition(original=original, expanded=parsed)
    if not isinstance(parsed, dict):
        return result

    high = parsed.get("high_level_description")
    comp = parsed.get("compositional_deconstruction") or {}
    elements = comp.get("elements") or [] if isinstance(comp, dict) else []
    if high or comp:
        result.is_structured = True
        result.high_level_description = high
        result.background = comp.get("background") if isinstance(comp, dict) else None
        for item in elements:
            if not isinstance(item, dict):
                continue
            result.elements.append(PromptElement(
                kind=str(item.get("type") or "unknown"),
                text=item.get("text"),
                description=item.get("desc") or item.get("description"),
                raw=dict(item),
            ))
    return result


def prompt_fingerprint(decomposition: PromptDecomposition) -> dict[str, Any]:
    kinds: dict[str, int] = {}
    for item in decomposition.elements:
        kinds[item.kind] = kinds.get(item.kind, 0) + 1
    return {
        "structured": decomposition.is_structured,
        "element_count": len(decomposition.elements),
        "element_kinds": kinds,
        "has_background": bool(decomposition.background),
        "has_high_level_description": bool(decomposition.high_level_description),
        "text_elements": sum(1 for e in decomposition.elements if e.text),
    }
