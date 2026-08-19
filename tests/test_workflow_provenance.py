import pytest

from content_universe.creativeos import (
    CheckpointStatus,
    CueMap,
    CuePoint,
    DeterministicMockBackend,
    OperationKind,
    OperationRequest,
    ProviderJobRecord,
    ReferenceBinding,
    ReferenceKind,
    ReferenceRole,
    ShotManifest,
    ShotSpec,
    SkillInvocationRecord,
    VerificationRecord,
    VerificationStatus,
    WorkflowCheckpoint,
    WorkflowHandoff,
    WorkflowRun,
    WorkflowRunStatus,
    persist_cue_map,
    persist_provider_job,
    persist_shot_manifest,
    persist_verification,
    persist_workflow_checkpoint,
    persist_workflow_handoff,
    persist_workflow_run,
)
from content_universe.models import CreativeEntity, EdgeKind, EntityKind, EntityRef
from content_universe.universe import ContentUniverse


def test_provider_job_preserves_execution_truthfulness() -> None:
    backend = DeterministicMockBackend({OperationKind.GENERATE})
    result = backend.execute(OperationRequest(operation=OperationKind.GENERATE))

    job = ProviderJobRecord.from_operation_result(
        workflow_run_id="run-1",
        result=result,
    )

    assert job.execution_mode.value == "mock"
    assert job.provider_call_performed is False
    assert job.requested_operation is OperationKind.GENERATE
    assert job.executed_operation is OperationKind.GENERATE


def test_passing_verification_requires_durable_evidence() -> None:
    with pytest.raises(ValueError, match="durable evidence"):
        VerificationRecord(
            verification_id="verify-1",
            workflow_run_id="run-1",
            subject=EntityRef(EntityKind.ASSET, "asset-1"),
            claim="asset exists",
            status=VerificationStatus.PASS,
        )


def test_music_to_video_workflow_persists_lineage() -> None:
    universe = ContentUniverse()
    track = universe.ingest_entity(
        CreativeEntity(entity_id="track-1", kind=EntityKind.TRACK, title="Synthetic Song")
    )
    evidence = universe.ingest_entity(
        CreativeEntity(entity_id="evidence-1", kind=EntityKind.FILE, title="render.mp4")
    )

    invocation = SkillInvocationRecord(
        invocation_id="invoke-1",
        skill_name="music-to-video",
        skill_version="1.0.0",
        semantic_capability="audiovisual_storyboarding",
        selected_workflow="music-to-video",
        tool_or_mcp="creativeos",
        provider_or_backend="mock",
        inputs=[track.ref],
    )
    run = WorkflowRun(
        workflow_run_id="run-1",
        workflow_name="music-to-video",
        status=WorkflowRunStatus.RUNNING,
        skill_invocations=[invocation],
        handoff_ids=["handoff-1"],
        checkpoint_ids=["checkpoint-1"],
        provider_job_ids=[],
        verification_ids=["verify-1"],
        inputs=[track.ref],
    )
    handoff = WorkflowHandoff(
        handoff_id="handoff-1",
        from_skill="brainstorming",
        to_skill="music-to-video",
        workflow_name="music-to-video",
        inputs=[track.ref],
        assumptions=["approved visual direction already supplied"],
    )
    checkpoint = WorkflowCheckpoint(
        checkpoint_id="checkpoint-1",
        workflow_run_id=run.workflow_run_id,
        phase="shot-planning",
        status=CheckpointStatus.COMPLETED,
        completed_steps=["cue-map", "shot-manifest"],
        artifacts=[track.ref],
    )

    cue_map = CueMap(
        cue_map_id="cue-map-1",
        source_track=track.ref,
        duration_seconds=30.0,
        cues=[
            CuePoint("cue-1", 0.0, 10.0, "intro", energy=0.2),
            CuePoint("cue-2", 10.0, 30.0, "chorus", energy=0.9),
        ],
        bpm=120,
    )
    shot_manifest = ShotManifest(
        shot_manifest_id="shots-1",
        workflow_run_id=run.workflow_run_id,
        cue_map_id=cue_map.cue_map_id,
        shots=[
            ShotSpec(
                shot_id="shot-1",
                scene_id="scene-1",
                cue_ids=["cue-1"],
                start_seconds=0.0,
                end_seconds=10.0,
                references=[
                    ReferenceBinding(
                        role=ReferenceRole.CONTINUITY,
                        kind=ReferenceKind.CHARACTER,
                        ref=EntityRef(EntityKind.CHARACTER, "hero-1"),
                    )
                ],
                protected_fields={"character_identity": "hero-1"},
            )
        ],
    )
    verification = VerificationRecord(
        verification_id="verify-1",
        workflow_run_id=run.workflow_run_id,
        subject=evidence.ref,
        claim="render artifact persisted",
        status=VerificationStatus.PASS,
        verification_type="artifact_exists",
        evidence=[evidence.ref],
    )

    persist_workflow_run(universe, run)
    persist_workflow_handoff(universe, handoff, workflow_run_id=run.workflow_run_id)
    persist_workflow_checkpoint(universe, checkpoint)
    persist_cue_map(universe, cue_map, workflow_run_id=run.workflow_run_id)
    persist_shot_manifest(universe, shot_manifest)
    persist_verification(universe, verification)

    kinds = {entity.kind for entity in universe.entities.values()}
    assert EntityKind.WORKFLOW_RUN in kinds
    assert EntityKind.SKILL_INVOCATION in kinds
    assert EntityKind.WORKFLOW_HANDOFF in kinds
    assert EntityKind.CHECKPOINT in kinds
    assert EntityKind.CUE_MAP in kinds
    assert EntityKind.SHOT_MANIFEST in kinds
    assert EntityKind.VERIFICATION in kinds

    edge_kinds = {edge.kind for edge in universe.graph.edges}
    assert EdgeKind.SELECTED_WORKFLOW in edge_kinds
    assert EdgeKind.CUE_MAP_FOR in edge_kinds
    assert EdgeKind.SHOT_PLAN_FOR in edge_kinds
    assert EdgeKind.VERIFIED_BY in edge_kinds


def test_provider_job_graph_connects_run_and_outputs() -> None:
    universe = ContentUniverse()
    backend = DeterministicMockBackend({OperationKind.GENERATE})
    result = backend.execute(OperationRequest(operation=OperationKind.GENERATE))
    job = ProviderJobRecord.from_operation_result(workflow_run_id="run-2", result=result)

    persist_provider_job(universe, job)

    provider_ref = EntityRef(EntityKind.PROVIDER_JOB, job.job_id)
    assert provider_ref.key in universe.entities
    assert any(
        edge.kind is EdgeKind.EXECUTED_AS and edge.target == provider_ref
        for edge in universe.graph.edges
    )
    assert any(
        edge.kind is EdgeKind.PRODUCED and edge.source == provider_ref
        for edge in universe.graph.edges
    )
