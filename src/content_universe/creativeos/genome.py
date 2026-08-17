from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from ..models import EntityRef
from .operations import ReferenceBinding
from .style import StyleDNA


@dataclass(slots=True)
class ReferenceGenomeEntry:
    entry_id: str
    title: str | None = None
    entity_ref: EntityRef | None = None
    references: list[ReferenceBinding] = field(default_factory=list)
    approved: bool = False
    notes: str | None = None
    metadata: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return {
            "entry_id": self.entry_id,
            "title": self.title,
            "entity_ref": (
                {"kind": self.entity_ref.kind.value, "id": self.entity_ref.id}
                if self.entity_ref is not None
                else None
            ),
            "references": [item.to_dict() for item in self.references],
            "approved": self.approved,
            "notes": self.notes,
            "metadata": self.metadata,
        }


@dataclass(slots=True)
class ReferenceGenome:
    """Reusable creative memory, not provider conditioning by default."""

    canon: dict[str, Any] = field(default_factory=dict)
    characters: dict[str, ReferenceGenomeEntry] = field(default_factory=dict)
    styles: dict[str, StyleDNA] = field(default_factory=dict)
    reference_sets: dict[str, list[ReferenceBinding]] = field(default_factory=dict)
    defaults: dict[str, Any] = field(default_factory=dict)
    metadata: dict[str, Any] = field(default_factory=dict)

    def add_character(self, key: str, entry: ReferenceGenomeEntry) -> ReferenceGenomeEntry:
        self.characters[key] = entry
        return entry

    def add_style(self, key: str, style: StyleDNA) -> StyleDNA:
        self.styles[key] = style
        return style

    def add_reference(self, set_name: str, reference: ReferenceBinding) -> ReferenceBinding:
        self.reference_sets.setdefault(set_name, []).append(reference)
        return reference

    def approved_characters(self) -> dict[str, ReferenceGenomeEntry]:
        return {key: value for key, value in self.characters.items() if value.approved}

    def to_dict(self) -> dict[str, Any]:
        return {
            "canon": self.canon,
            "characters": {key: value.to_dict() for key, value in self.characters.items()},
            "styles": {key: value.to_dict() for key, value in self.styles.items()},
            "reference_sets": {
                key: [item.to_dict() for item in values]
                for key, values in self.reference_sets.items()
            },
            "defaults": self.defaults,
            "metadata": self.metadata,
        }
