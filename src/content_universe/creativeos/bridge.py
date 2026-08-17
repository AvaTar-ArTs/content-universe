from __future__ import annotations

from ..graph import GraphEdge
from ..models import CreativeEntity, EdgeKind, EntityKind, EntityRef
from ..universe import ContentUniverse
from .evaluation import ApprovalRecord, EvaluationRecord
from .genome import ReferenceGenome
from .prompt import PromptManifest
from .scene import SceneGraph
from .style import StyleDNA


def _ingest_contract_entity(
    universe: ContentUniverse,
    *,
    entity_id: str,
    kind: EntityKind,
    payload: dict,
    source: str,
    title: str | None = None,
    description: str | None = None,
) -> CreativeEntity:
    return universe.ingest_entity(
        CreativeEntity(
            entity_id=entity_id,
            kind=kind,
            title=title,
            description=description,
            metadata={"contract": payload},
            sources=[source],
        )
    )


def persist_prompt_manifest(
    universe: ContentUniverse,
    manifest: PromptManifest,
    *,
    source: str = "creativeos",
) -> CreativeEntity:
    entity = _ingest_contract_entity(
        universe,
        entity_id=manifest.manifest_id,
        kind=EntityKind.PROMPT_MANIFEST,
        payload=manifest.to_dict(),
        source=source,
        title=manifest.purpose,
        description=manifest.brief,
    )
    if manifest.scene is not None:
        scene_id = f"{manifest.manifest_id}:scene"
        scene_entity = persist_scene_graph(universe, scene_id, manifest.scene, source=source)
        universe.graph.add(GraphEdge(entity.ref, scene_entity.ref, EdgeKind.EXPANDED_INTO))
    return entity


def persist_scene_graph(
    universe: ContentUniverse,
    scene_id: str,
    scene: SceneGraph,
    *,
    source: str = "creativeos",
) -> CreativeEntity:
    entity = _ingest_contract_entity(
        universe,
        entity_id=scene_id,
        kind=EntityKind.SCENE_GRAPH,
        payload=scene.to_dict(),
        source=source,
        description=scene.high_level_description,
    )
    for element in scene.elements:
        if element.entity_ref is None:
            continue
        universe.graph.add(
            GraphEdge(
                entity.ref,
                element.entity_ref,
                EdgeKind.INSTANCE_OF,
                {
                    "element_id": element.element_id,
                    "element_kind": element.kind.value,
                    "text": element.text,
                },
            )
        )
    return entity


def persist_style_dna(
    universe: ContentUniverse,
    style_id: str,
    style: StyleDNA,
    *,
    source: str = "creativeos",
) -> CreativeEntity:
    return _ingest_contract_entity(
        universe,
        entity_id=style_id,
        kind=EntityKind.STYLE_DNA,
        payload=style.to_dict(),
        source=source,
        title=style.name,
    )


def persist_reference_genome(
    universe: ContentUniverse,
    genome_id: str,
    genome: ReferenceGenome,
    *,
    source: str = "creativeos",
) -> CreativeEntity:
    return _ingest_contract_entity(
        universe,
        entity_id=genome_id,
        kind=EntityKind.REFERENCE_GENOME,
        payload=genome.to_dict(),
        source=source,
    )


def persist_evaluation(
    universe: ContentUniverse,
    evaluation: EvaluationRecord,
    *,
    source: str = "creativeos",
) -> CreativeEntity:
    entity = _ingest_contract_entity(
        universe,
        entity_id=evaluation.evaluation_id,
        kind=EntityKind.EVALUATION,
        payload=evaluation.to_dict(),
        source=source,
        title=evaluation.kind.value,
    )
    universe.graph.add(GraphEdge(evaluation.subject, entity.ref, EdgeKind.EVALUATED_BY))
    return entity


def persist_approval(
    universe: ContentUniverse,
    approval: ApprovalRecord,
    *,
    source: str = "creativeos",
) -> CreativeEntity:
    entity = _ingest_contract_entity(
        universe,
        entity_id=approval.approval_id,
        kind=EntityKind.APPROVAL,
        payload=approval.to_dict(),
        source=source,
        title=approval.status.value,
    )
    universe.graph.add(GraphEdge(approval.subject, entity.ref, EdgeKind.APPROVED_AS))
    for evaluation_id in approval.evaluation_ids:
        universe.graph.add(
            GraphEdge(
                EntityRef(EntityKind.EVALUATION, evaluation_id),
                entity.ref,
                EdgeKind.RELATED_TO,
            )
        )
    return entity
