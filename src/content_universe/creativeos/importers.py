from __future__ import annotations

from typing import Any

from ..promptlab import PromptDecomposition
from .prompt import PromptLineage, PromptManifest, PromptRevision, PromptStage
from .scene import SceneElement, SceneElementKind, SceneGraph


_KIND_MAP = {
    "obj": SceneElementKind.OBJECT,
    "object": SceneElementKind.OBJECT,
    "text": SceneElementKind.TEXT,
    "graphic": SceneElementKind.GRAPHIC,
    "panel": SceneElementKind.PANEL,
    "environment": SceneElementKind.ENVIRONMENT,
    "effect": SceneElementKind.EFFECT,
    "region": SceneElementKind.REGION,
}


def scene_graph_from_prompt_decomposition(decomposition: PromptDecomposition) -> SceneGraph:
    """Normalize recovered/provider prompt structure into a portable SceneGraph.

    Unknown provider fields remain in element metadata rather than being silently
    discarded or promoted into provider-neutral semantics without evidence.
    """

    scene = SceneGraph(
        high_level_description=decomposition.high_level_description,
        background=decomposition.background,
        provider_metadata={"structured_prompt": decomposition.is_structured},
    )
    for index, item in enumerate(decomposition.elements):
        kind = _KIND_MAP.get(item.kind.lower(), SceneElementKind.UNKNOWN)
        scene.add_element(
            SceneElement(
                element_id=f"element-{index + 1}",
                kind=kind,
                description=item.description,
                text=item.text,
                metadata={"provider_raw": dict(item.raw)},
            )
        )
    return scene


def prompt_manifest_from_decomposition(
    manifest_id: str,
    decomposition: PromptDecomposition,
    *,
    source: str = "recovered-provider-prompt",
    metadata: dict[str, Any] | None = None,
) -> PromptManifest:
    lineage: PromptLineage | None = None
    if decomposition.original is not None:
        lineage = PromptLineage(original=decomposition.original)
        if decomposition.expanded not in (None, "", {}, []):
            lineage = lineage.append(
                PromptRevision(
                    stage=PromptStage.PROVIDER_EXPANDED,
                    value=decomposition.expanded,
                    source=source,
                )
            )

    return PromptManifest(
        manifest_id=manifest_id,
        lineage=lineage,
        scene=scene_graph_from_prompt_decomposition(decomposition),
        metadata=dict(metadata or {}),
    )
