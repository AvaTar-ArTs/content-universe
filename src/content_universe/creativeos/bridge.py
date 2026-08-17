from __future__ import annotations

from ..graph import GraphEdge
from ..models import CreativeEntity, EdgeKind, EntityKind, EntityRef
from ..universe import ContentUniverse
from .audiovisual import CueMap, ShotManifest
from .design_asset import StructuredDesignAsset
from .evaluation import ApprovalRecord, EvaluationRecord
from .genome import ReferenceGenome
from .prompt import PromptManifest
from .scene import SceneGraph
from .style import StyleDNA
from .workflow import (
    ProviderJobRecord,
    SkillInvocationRecord,
    VerificationRecord,
    WorkflowCheckpoint,
    WorkflowHandoff,
    WorkflowRun,
)


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
                edge_id=element.element_id,
            )
        )
    return entity


def persist_structured_design_asset(
    universe: ContentUniverse,
    design: StructuredDesignAsset,
    *,
    source: str = "creativeos",
) -> CreativeEntity:
    entity = _ingest_contract_entity(
        universe,
        entity_id=design.design_id,
        kind=EntityKind.STRUCTURED_DESIGN_ASSET,
        payload=design.to_dict(),
        source=source,
    )
    if design.base_asset is not None:
        universe.graph.add(GraphEdge(entity.ref, design.base_asset, EdgeKind.USES, {"role": "base_asset"}))
    if design.scene_graph_id:
        universe.graph.add(
            GraphEdge(entity.ref, EntityRef(EntityKind.SCENE_GRAPH, design.scene_graph_id), EdgeKind.USES, {"role": "scene_graph"})
        )
    if design.prompt_manifest_id:
        prompt_ref = EntityRef(EntityKind.PROMPT_MANIFEST, design.prompt_manifest_id)
        universe.graph.add(GraphEdge(prompt_ref, entity.ref, EdgeKind.RENDERED_AS))
    for style_id in design.style_dna_ids:
        universe.graph.add(
            GraphEdge(entity.ref, EntityRef(EntityKind.STYLE_DNA, style_id), EdgeKind.USES, {"role": "style_dna"})
        )
    for vector_ref in design.vector_assets:
        universe.graph.add(GraphEdge(entity.ref, vector_ref, EdgeKind.USES, {"role": "vector_asset"}))
    if design.parent_design is not None:
        universe.graph.add(GraphEdge(entity.ref, design.parent_design, EdgeKind.DERIVED_FROM))
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


def persist_workflow_run(
    universe: ContentUniverse,
    run: WorkflowRun,
    *,
    source: str = "agent-skills",
) -> CreativeEntity:
    entity = _ingest_contract_entity(
        universe,
        entity_id=run.workflow_run_id,
        kind=EntityKind.WORKFLOW_RUN,
        payload=run.to_dict(),
        source=source,
        title=run.workflow_name,
        description=run.status.value,
    )
    workflow_ref = EntityRef(EntityKind.WORKFLOW, run.workflow_name)
    universe.graph.add(GraphEdge(entity.ref, workflow_ref, EdgeKind.SELECTED_WORKFLOW))
    if run.parent_run_id:
        universe.graph.add(
            GraphEdge(entity.ref, EntityRef(EntityKind.WORKFLOW_RUN, run.parent_run_id), EdgeKind.RESUMES)
        )
    for ref in run.inputs:
        universe.graph.add(GraphEdge(entity.ref, ref, EdgeKind.USES, {"role": "workflow_input"}))
    for ref in run.outputs:
        universe.graph.add(GraphEdge(entity.ref, ref, EdgeKind.PRODUCED, {"role": "workflow_output"}))
    for invocation in run.skill_invocations:
        invocation_entity = persist_skill_invocation(
            universe,
            invocation,
            workflow_run_id=run.workflow_run_id,
            source=source,
        )
        universe.graph.add(GraphEdge(entity.ref, invocation_entity.ref, EdgeKind.INVOKED_AS))
    for handoff_id in run.handoff_ids:
        universe.graph.add(
            GraphEdge(entity.ref, EntityRef(EntityKind.WORKFLOW_HANDOFF, handoff_id), EdgeKind.RELATED_TO)
        )
    for checkpoint_id in run.checkpoint_ids:
        universe.graph.add(
            GraphEdge(EntityRef(EntityKind.CHECKPOINT, checkpoint_id), entity.ref, EdgeKind.CHECKPOINT_OF)
        )
    for job_id in run.provider_job_ids:
        universe.graph.add(
            GraphEdge(entity.ref, EntityRef(EntityKind.PROVIDER_JOB, job_id), EdgeKind.EXECUTED_AS)
        )
    for verification_id in run.verification_ids:
        universe.graph.add(
            GraphEdge(entity.ref, EntityRef(EntityKind.VERIFICATION, verification_id), EdgeKind.VERIFIED_BY)
        )
    return entity


def persist_skill_invocation(
    universe: ContentUniverse,
    invocation: SkillInvocationRecord,
    *,
    workflow_run_id: str | None = None,
    source: str = "agent-skills",
) -> CreativeEntity:
    entity = _ingest_contract_entity(
        universe,
        entity_id=invocation.invocation_id,
        kind=EntityKind.SKILL_INVOCATION,
        payload=invocation.to_dict(),
        source=source,
        title=invocation.skill_name,
        description=invocation.semantic_capability,
    )
    if workflow_run_id:
        universe.graph.add(
            GraphEdge(EntityRef(EntityKind.WORKFLOW_RUN, workflow_run_id), entity.ref, EdgeKind.INVOKED_AS)
        )
    for ref in invocation.inputs:
        universe.graph.add(GraphEdge(entity.ref, ref, EdgeKind.USES, {"role": "skill_input"}))
    for ref in invocation.outputs:
        universe.graph.add(GraphEdge(entity.ref, ref, EdgeKind.PRODUCED, {"role": "skill_output"}))
    return entity


def persist_workflow_handoff(
    universe: ContentUniverse,
    handoff: WorkflowHandoff,
    *,
    workflow_run_id: str | None = None,
    source: str = "agent-skills",
) -> CreativeEntity:
    entity = _ingest_contract_entity(
        universe,
        entity_id=handoff.handoff_id,
        kind=EntityKind.WORKFLOW_HANDOFF,
        payload=handoff.to_dict(),
        source=source,
        title=f"{handoff.from_skill} -> {handoff.to_skill}",
        description=handoff.workflow_name,
    )
    if workflow_run_id:
        universe.graph.add(
            GraphEdge(EntityRef(EntityKind.WORKFLOW_RUN, workflow_run_id), entity.ref, EdgeKind.HANDED_OFF_TO)
        )
    if handoff.approved_design is not None:
        universe.graph.add(GraphEdge(entity.ref, handoff.approved_design, EdgeKind.USES, {"role": "approved_design"}))
    for ref in handoff.inputs:
        universe.graph.add(GraphEdge(entity.ref, ref, EdgeKind.USES, {"role": "handoff_input"}))
    for ref in handoff.outputs:
        universe.graph.add(GraphEdge(entity.ref, ref, EdgeKind.PRODUCED, {"role": "handoff_output"}))
    return entity


def persist_workflow_checkpoint(
    universe: ContentUniverse,
    checkpoint: WorkflowCheckpoint,
    *,
    source: str = "agent-skills",
) -> CreativeEntity:
    entity = _ingest_contract_entity(
        universe,
        entity_id=checkpoint.checkpoint_id,
        kind=EntityKind.CHECKPOINT,
        payload=checkpoint.to_dict(),
        source=source,
        title=checkpoint.phase,
        description=checkpoint.status.value,
    )
    universe.graph.add(
        GraphEdge(entity.ref, EntityRef(EntityKind.WORKFLOW_RUN, checkpoint.workflow_run_id), EdgeKind.CHECKPOINT_OF)
    )
    for ref in checkpoint.artifacts:
        universe.graph.add(GraphEdge(entity.ref, ref, EdgeKind.USES, {"role": "checkpoint_artifact"}))
    return entity


def persist_provider_job(
    universe: ContentUniverse,
    job: ProviderJobRecord,
    *,
    source: str = "creativeos",
) -> CreativeEntity:
    entity = _ingest_contract_entity(
        universe,
        entity_id=job.job_id,
        kind=EntityKind.PROVIDER_JOB,
        payload=job.to_dict(),
        source=source,
        title=job.provider or job.execution_mode.value,
        description=job.status.value,
    )
    universe.graph.add(
        GraphEdge(EntityRef(EntityKind.WORKFLOW_RUN, job.workflow_run_id), entity.ref, EdgeKind.EXECUTED_AS)
    )
    if job.checkpoint_id:
        universe.graph.add(
            GraphEdge(EntityRef(EntityKind.CHECKPOINT, job.checkpoint_id), entity.ref, EdgeKind.EXECUTED_AS)
        )
    for ref in job.inputs:
        universe.graph.add(GraphEdge(entity.ref, ref, EdgeKind.USES, {"role": "provider_input"}))
    for ref in job.outputs:
        universe.graph.add(GraphEdge(entity.ref, ref, EdgeKind.PRODUCED, {"role": "provider_output"}))
    return entity


def persist_verification(
    universe: ContentUniverse,
    verification: VerificationRecord,
    *,
    source: str = "creativeos",
) -> CreativeEntity:
    entity = _ingest_contract_entity(
        universe,
        entity_id=verification.verification_id,
        kind=EntityKind.VERIFICATION,
        payload=verification.to_dict(),
        source=source,
        title=verification.verification_type or "verification",
        description=verification.status.value,
    )
    universe.graph.add(GraphEdge(verification.subject, entity.ref, EdgeKind.VERIFIED_BY))
    universe.graph.add(
        GraphEdge(EntityRef(EntityKind.WORKFLOW_RUN, verification.workflow_run_id), entity.ref, EdgeKind.VERIFIED_BY)
    )
    for ref in verification.evidence:
        universe.graph.add(GraphEdge(entity.ref, ref, EdgeKind.USES, {"role": "verification_evidence"}))
    return entity


def persist_cue_map(
    universe: ContentUniverse,
    cue_map: CueMap,
    *,
    workflow_run_id: str | None = None,
    source: str = "creativeos",
) -> CreativeEntity:
    entity = _ingest_contract_entity(
        universe,
        entity_id=cue_map.cue_map_id,
        kind=EntityKind.CUE_MAP,
        payload=cue_map.to_dict(),
        source=source,
        title="audiovisual cue map",
        description=f"{cue_map.duration_seconds:.3f}s",
    )
    universe.graph.add(GraphEdge(entity.ref, cue_map.source_track, EdgeKind.CUE_MAP_FOR))
    if workflow_run_id:
        universe.graph.add(
            GraphEdge(EntityRef(EntityKind.WORKFLOW_RUN, workflow_run_id), entity.ref, EdgeKind.PRODUCED)
        )
    return entity


def persist_shot_manifest(
    universe: ContentUniverse,
    manifest: ShotManifest,
    *,
    source: str = "creativeos",
) -> CreativeEntity:
    entity = _ingest_contract_entity(
        universe,
        entity_id=manifest.shot_manifest_id,
        kind=EntityKind.SHOT_MANIFEST,
        payload=manifest.to_dict(),
        source=source,
        title="shot manifest",
        description=manifest.review_status,
    )
    universe.graph.add(
        GraphEdge(EntityRef(EntityKind.WORKFLOW_RUN, manifest.workflow_run_id), entity.ref, EdgeKind.SHOT_PLAN_FOR)
    )
    universe.graph.add(
        GraphEdge(entity.ref, EntityRef(EntityKind.CUE_MAP, manifest.cue_map_id), EdgeKind.USES, {"role": "cue_map"})
    )
    for shot in manifest.shots:
        if shot.prompt_manifest_id:
            universe.graph.add(
                GraphEdge(
                    entity.ref,
                    EntityRef(EntityKind.PROMPT_MANIFEST, shot.prompt_manifest_id),
                    EdgeKind.USES,
                    {"role": "shot_prompt", "shot_id": shot.shot_id},
                    edge_id=f"{shot.shot_id}:prompt",
                )
            )
        if shot.scene_graph_id:
            universe.graph.add(
                GraphEdge(
                    entity.ref,
                    EntityRef(EntityKind.SCENE_GRAPH, shot.scene_graph_id),
                    EdgeKind.USES,
                    {"role": "shot_scene", "shot_id": shot.shot_id},
                    edge_id=f"{shot.shot_id}:scene",
                )
            )
        for index, reference in enumerate(shot.references):
            if reference.ref is None:
                continue
            universe.graph.add(
                GraphEdge(
                    entity.ref,
                    reference.ref,
                    EdgeKind.USES,
                    {
                        "role": f"shot_reference:{reference.role.value}",
                        "reference_kind": reference.kind.value,
                        "shot_id": shot.shot_id,
                    },
                    edge_id=f"{shot.shot_id}:reference:{index}",
                )
            )
    return entity
