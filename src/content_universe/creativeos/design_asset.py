from __future__ import annotations

from dataclasses import asdict, dataclass, field
from typing import Any

from ..models import EntityRef
from .scene import BoundingBox


@dataclass(slots=True)
class Mask:
    """Semantic/edit mask associated with a structured design asset."""

    mask_id: str
    asset_ref: EntityRef | None = None
    bounds: BoundingBox | None = None
    purpose: str | None = None
    metadata: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return {
            "mask_id": self.mask_id,
            "asset_ref": (
                {"kind": self.asset_ref.kind.value, "id": self.asset_ref.id}
                if self.asset_ref is not None
                else None
            ),
            "bounds": asdict(self.bounds) if self.bounds else None,
            "purpose": self.purpose,
            "metadata": self.metadata,
        }


@dataclass(slots=True)
class GenerationWindow:
    """A target region intended for generation/editing without replacing the whole design."""

    window_id: str
    bounds: BoundingBox
    element_ids: list[str] = field(default_factory=list)
    operation_hint: str | None = None
    locked_element_ids: list[str] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return {
            "window_id": self.window_id,
            "bounds": asdict(self.bounds),
            "element_ids": self.element_ids,
            "operation_hint": self.operation_hint,
            "locked_element_ids": self.locked_element_ids,
            "metadata": self.metadata,
        }


@dataclass(slots=True)
class StructuredDesignAsset:
    """Editable creative object layered above one or more raster/vector assets.

    IDs reference durable Content Universe objects rather than embedding provider
    URLs as canonical identity.
    """

    design_id: str
    base_asset: EntityRef | None = None
    scene_graph_id: str | None = None
    prompt_manifest_id: str | None = None
    style_dna_ids: list[str] = field(default_factory=list)
    vector_assets: list[EntityRef] = field(default_factory=list)
    masks: list[Mask] = field(default_factory=list)
    generation_windows: list[GenerationWindow] = field(default_factory=list)
    parent_design: EntityRef | None = None
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        if not self.design_id:
            raise ValueError("StructuredDesignAsset requires design_id")

    def to_dict(self) -> dict[str, Any]:
        return {
            "design_id": self.design_id,
            "base_asset": (
                {"kind": self.base_asset.kind.value, "id": self.base_asset.id}
                if self.base_asset is not None
                else None
            ),
            "scene_graph_id": self.scene_graph_id,
            "prompt_manifest_id": self.prompt_manifest_id,
            "style_dna_ids": self.style_dna_ids,
            "vector_assets": [
                {"kind": item.kind.value, "id": item.id} for item in self.vector_assets
            ],
            "masks": [item.to_dict() for item in self.masks],
            "generation_windows": [item.to_dict() for item in self.generation_windows],
            "parent_design": (
                {"kind": self.parent_design.kind.value, "id": self.parent_design.id}
                if self.parent_design is not None
                else None
            ),
            "metadata": self.metadata,
        }
