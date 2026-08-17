from __future__ import annotations

from dataclasses import asdict, dataclass, field
from enum import StrEnum
from typing import Any

from .operations import ReferenceBinding


class StyleSourceKind(StrEnum):
    PROMPT_KEYWORD = "prompt_keyword"
    MODEL_MODE = "model_mode"
    PROVIDER_PRESET = "provider_preset"
    IMAGE_REFERENCE = "image_reference"
    SAVED_STYLE = "saved_style"
    QUICK_REFERENCE = "quick_reference"
    CUSTOM_MODEL = "custom_model"
    STYLE_DNA = "style_dna"
    PALETTE = "palette"
    TYPOGRAPHY = "typography"
    OTHER = "other"


@dataclass(slots=True)
class StyleDNA:
    """Portable style description independent of a single provider preset."""

    name: str | None = None
    palette: list[str] = field(default_factory=list)
    typography: dict[str, Any] = field(default_factory=dict)
    composition: dict[str, Any] = field(default_factory=dict)
    motifs: list[str] = field(default_factory=list)
    materials: list[str] = field(default_factory=list)
    techniques: list[str] = field(default_factory=list)
    exclusions: list[str] = field(default_factory=list)
    descriptors: list[str] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(slots=True)
class StyleLayer:
    source_kind: StyleSourceKind
    name: str | None = None
    value: Any = None
    reference: ReferenceBinding | None = None
    provider: str | None = None
    weight: float | None = None
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        if self.weight is not None and self.weight < 0:
            raise ValueError("style weight cannot be negative")
        if self.value is None and self.reference is None and not self.name:
            raise ValueError("style layer requires a name, value, or reference")

    def to_dict(self) -> dict[str, Any]:
        return {
            "source_kind": self.source_kind.value,
            "name": self.name,
            "value": self.value.to_dict() if isinstance(self.value, StyleDNA) else self.value,
            "reference": self.reference.to_dict() if self.reference else None,
            "provider": self.provider,
            "weight": self.weight,
            "metadata": self.metadata,
        }


@dataclass(slots=True)
class StyleStack:
    """Ordered style sources that must not be flattened into one label."""

    layers: list[StyleLayer] = field(default_factory=list)

    def add(self, layer: StyleLayer) -> StyleLayer:
        self.layers.append(layer)
        return layer

    def by_source(self, source_kind: StyleSourceKind) -> list[StyleLayer]:
        return [item for item in self.layers if item.source_kind is source_kind]

    def to_dict(self) -> dict[str, Any]:
        return {"layers": [item.to_dict() for item in self.layers]}
