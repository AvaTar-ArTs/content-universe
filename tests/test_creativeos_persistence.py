import pytest

from content_universe.creativeos import (
    ApprovalRecord,
    ApprovalStatus,
    EvaluationKind,
    EvaluationRecord,
    PromptLineage,
    PromptManifest,
    ReferenceGenome,
    StyleDNA,
    persist_approval,
    persist_evaluation,
    persist_prompt_manifest,
    persist_reference_genome,
    persist_style_dna,
)
from content_universe.models import EdgeKind, EntityKind, EntityRef
from content_universe.universe import ContentUniverse


def test_prompt_manifest_persists_with_scene_child() -> None:
    manifest = PromptManifest(
        manifest_id="prompt-1",
        brief="Cover brief",
        lineage=PromptLineage(original="make a cover"),
    )
    universe = ContentUniverse()
    entity = persist_prompt_manifest(universe, manifest)

    assert entity.kind is EntityKind.PROMPT_MANIFEST
    assert universe.entities[entity.ref.key].metadata["contract"]["lineage"]["original"] == "make a cover"


def test_style_and_reference_genome_persist_as_typed_entities() -> None:
    universe = ContentUniverse()
    style = persist_style_dna(universe, "style-1", StyleDNA(name="Nocturne"))
    genome = persist_reference_genome(universe, "genome-1", ReferenceGenome())

    assert style.kind is EntityKind.STYLE_DNA
    assert genome.kind is EntityKind.REFERENCE_GENOME


def test_evaluation_and_approval_create_graph_edges() -> None:
    universe = ContentUniverse()
    subject = EntityRef(EntityKind.ASSET, "asset-1")
    evaluation = EvaluationRecord(
        evaluation_id="eval-1",
        subject=subject,
        kind=EvaluationKind.STYLE_CONSISTENCY,
        score=0.9,
    )
    approval = ApprovalRecord(
        approval_id="approval-1",
        subject=subject,
        status=ApprovalStatus.APPROVED,
        evaluation_ids=[evaluation.evaluation_id],
    )

    eval_entity = persist_evaluation(universe, evaluation)
    approval_entity = persist_approval(universe, approval)

    assert eval_entity.kind is EntityKind.EVALUATION
    assert approval_entity.kind is EntityKind.APPROVAL
    assert any(edge.kind is EdgeKind.EVALUATED_BY for edge in universe.graph.edges)
    assert any(edge.kind is EdgeKind.APPROVED_AS for edge in universe.graph.edges)


def test_evaluation_score_must_be_normalized() -> None:
    with pytest.raises(ValueError):
        EvaluationRecord(
            evaluation_id="bad",
            subject=EntityRef(EntityKind.ASSET, "asset-1"),
            kind=EvaluationKind.QUALITY,
            score=2.0,
        )
