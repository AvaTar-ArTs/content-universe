from __future__ import annotations

from dataclasses import dataclass, field, replace
from enum import StrEnum
from typing import Any

from .operations import ReferenceBinding
from .scene import SceneGraph
from .style import StyleStack


class PromptStage(StrEnum):
    ENHANCED = "enhanced"
    PROVIDER_DIALECT = "provider_dialect"
    PROVIDER_EXPANDED = "provider_expanded"
    LOCALIZED = "localized"
    REFLOWED = "reflowed"
    DESCRIPTION = "description"
    MANUAL_REVISION = "manual_revision"


@dataclass(slots=True, frozen=True)
class PromptRevision:
    stage: PromptStage
    value: Any
    source: str | None = None
    metadata: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return {
            "stage": self.stage.value,
            "value": self.value,
            "source": self.source,
            "metadata": self.metadata,
        }


@dataclass(slots=True, frozen=True)
class PromptLineage:
    """Immutable prompt history that preserves creator intent.

    Adding an enhancement/provider expansion returns a new lineage object. The
    original prompt can therefore never be overwritten as a side effect.
    """

    original: str
    revisions: tuple[PromptRevision, ...] = ()

    def append(self, revision: PromptRevision) -> PromptLineage:
        return replace(self, revisions=self.revisions + (revision,))

    @property
    def latest(self) -> Any:
        return self.revisions[-1].value if self.revisions else self.original

    def by_stage(self, stage: PromptStage) -> tuple[PromptRevision, ...]:
        return tuple(item for item in self.revisions if item.stage is stage)

    def to_dict(self) -> dict[str, Any]:
        return {
            "original": self.original,
            "revisions": [item.to_dict() for item in self.revisions],
        }


@dataclass(slots=True)
class PromptManifest:
    manifest_id: str
    brief: str | None = None
    lineage: PromptLineage | None = None
    scene: SceneGraph | None = None
    styles: StyleStack = field(default_factory=StyleStack)
    references: list[ReferenceBinding] = field(default_factory=list)
    exclusions: list[str] = field(default_factory=list)
    purpose: str | None = None
    output_channel: str | None = None
    aspect_ratio: str | None = None
    dimensions: tuple[int, int] | None = None
    constraints: dict[str, Any] = field(default_factory=dict)
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        if self.dimensions is not None:
            width, height = self.dimensions
            if width <= 0 or height <= 0:
                raise ValueError("prompt-manifest dimensions must be positive")

    @property
    def original_prompt(self) -> str | None:
        return self.lineage.original if self.lineage else None

    def to_dict(self) -> dict[str, Any]:
        return {
            "manifest_id": self.manifest_id,
            "brief": self.brief,
            "lineage": self.lineage.to_dict() if self.lineage else None,
            "scene": self.scene.to_dict() if self.scene else None,
            "styles": self.styles.to_dict(),
            "references": [item.to_dict() for item in self.references],
            "exclusions": self.exclusions,
            "purpose": self.purpose,
            "output_channel": self.output_channel,
            "aspect_ratio": self.aspect_ratio,
            "dimensions": list(self.dimensions) if self.dimensions else None,
            "constraints": self.constraints,
            "metadata": self.metadata,
        }
