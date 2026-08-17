from __future__ import annotations

from dataclasses import asdict, dataclass, field
from enum import StrEnum
from typing import Any

from ..models import EntityRef
from .operations import ReferenceBinding


class SceneElementKind(StrEnum):
    OBJECT = "object"
    TEXT = "text"
    GRAPHIC = "graphic"
    PANEL = "panel"
    ENVIRONMENT = "environment"
    EFFECT = "effect"
    REGION = "region"
    UNKNOWN = "unknown"


@dataclass(slots=True, frozen=True)
class BoundingBox:
    x: float
    y: float
    width: float
    height: float
    coordinate_space: str = "normalized"

    def __post_init__(self) -> None:
        if self.width < 0 or self.height < 0:
            raise ValueError("bounding-box width/height cannot be negative")
        if self.coordinate_space == "normalized":
            values = (self.x, self.y, self.width, self.height)
            if any(value < 0 or value > 1 for value in values):
                raise ValueError("normalized bounding-box coordinates must be between 0 and 1")


@dataclass(slots=True)
class TypographyLayer:
    text: str
    font_family: str | None = None
    font_style: str | None = None
    weight: int | str | None = None
    size: float | None = None
    color: str | None = None
    alignment: str | None = None
    tracking: float | None = None
    line_height: float | None = None
    rotation: float | None = None
    editable: bool = True
    metadata: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(slots=True)
class SceneElement:
    element_id: str
    kind: SceneElementKind
    description: str | None = None
    text: str | None = None
    bounds: BoundingBox | None = None
    typography: TypographyLayer | None = None
    entity_ref: EntityRef | None = None
    references: list[ReferenceBinding] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        if self.kind is SceneElementKind.TEXT and self.typography is not None and self.text is None:
            self.text = self.typography.text
        if self.typography is not None and self.kind is not SceneElementKind.TEXT:
            raise ValueError("TypographyLayer may only be attached to a text SceneElement")

    def to_dict(self) -> dict[str, Any]:
        return {
            "element_id": self.element_id,
            "kind": self.kind.value,
            "description": self.description,
            "text": self.text,
            "bounds": asdict(self.bounds) if self.bounds else None,
            "typography": self.typography.to_dict() if self.typography else None,
            "entity_ref": (
                {"kind": self.entity_ref.kind.value, "id": self.entity_ref.id}
                if self.entity_ref is not None
                else None
            ),
            "references": [item.to_dict() for item in self.references],
            "metadata": self.metadata,
        }


@dataclass(slots=True)
class SceneGraph:
    high_level_description: str | None = None
    background: str | None = None
    elements: list[SceneElement] = field(default_factory=list)
    references: list[ReferenceBinding] = field(default_factory=list)
    provider_metadata: dict[str, Any] = field(default_factory=dict)
    metadata: dict[str, Any] = field(default_factory=dict)

    def add_element(self, element: SceneElement) -> SceneElement:
        if any(existing.element_id == element.element_id for existing in self.elements):
            raise ValueError(f"duplicate scene element id: {element.element_id}")
        self.elements.append(element)
        return element

    def get_element(self, element_id: str) -> SceneElement | None:
        return next((item for item in self.elements if item.element_id == element_id), None)

    def to_dict(self) -> dict[str, Any]:
        return {
            "high_level_description": self.high_level_description,
            "background": self.background,
            "elements": [item.to_dict() for item in self.elements],
            "references": [item.to_dict() for item in self.references],
            "provider_metadata": self.provider_metadata,
            "metadata": self.metadata,
        }
