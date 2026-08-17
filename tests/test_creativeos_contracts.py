from dataclasses import FrozenInstanceError

import pytest

from content_universe.creativeos.importers import prompt_manifest_from_decomposition
from content_universe.creativeos.operations import (
    ExecutionMode,
    OperationKind,
    OperationRequest,
    OperationResult,
    ReferenceBinding,
    ReferenceKind,
    ReferenceRole,
)
from content_universe.creativeos.prompt import PromptLineage, PromptRevision, PromptStage
from content_universe.creativeos.provider import DeterministicMockBackend, ProviderRegistry
from content_universe.creativeos.scene import SceneElementKind
from content_universe.creativeos.style import StyleDNA, StyleLayer, StyleSourceKind, StyleStack
from content_universe.models import EntityKind, EntityRef
from content_universe.promptlab import decompose_prompt


def asset_ref(asset_id: str = "asset-1") -> EntityRef:
    return EntityRef(EntityKind.ASSET, asset_id)


def test_operation_source_cardinality() -> None:
    OperationRequest(OperationKind.GENERATE)
    OperationRequest(OperationKind.EDIT, sources=[asset_ref()])
    OperationRequest(OperationKind.REMIX, sources=[asset_ref()])
    with pytest.raises(ValueError):
        OperationRequest(OperationKind.GENERATE, sources=[asset_ref()])
    with pytest.raises(ValueError):
        OperationRequest(OperationKind.REMIX)
    with pytest.raises(ValueError):
        OperationRequest(OperationKind.UPSCALE, sources=[asset_ref("a"), asset_ref("b")])


def test_reference_roles_are_separate() -> None:
    authoring = ReferenceBinding(
        role=ReferenceRole.AUTHORING,
        kind=ReferenceKind.COMPOSITION,
        ref=asset_ref("layout-guide"),
    )
    generation = ReferenceBinding(
        role=ReferenceRole.GENERATION,
        kind=ReferenceKind.STYLE,
        ref=asset_ref("style-ref"),
    )
    request = OperationRequest(OperationKind.GENERATE, references=[authoring, generation])
    assert request.generation_references == [generation]


def test_result_operation_must_match_request() -> None:
    with pytest.raises(ValueError):
        OperationResult(
            requested_operation=OperationKind.REMIX,
            executed_operation=OperationKind.GENERATE,
            execution_mode=ExecutionMode.MOCK,
        )


def test_mock_result_cannot_be_marked_provider_execution() -> None:
    with pytest.raises(ValueError):
        OperationResult(
            requested_operation=OperationKind.GENERATE,
            executed_operation=OperationKind.GENERATE,
            execution_mode=ExecutionMode.MOCK,
            provider_call_performed=True,
        )


def test_prompt_lineage_preserves_original() -> None:
    original = PromptLineage(original="rough creator prompt")
    enhanced = original.append(PromptRevision(PromptStage.ENHANCED, "expanded instructions", source="local"))
    assert original.revisions == ()
    assert enhanced.original == "rough creator prompt"
    assert enhanced.latest == "expanded instructions"
    with pytest.raises(FrozenInstanceError):
        enhanced.original = "replacement"


def test_style_stack_keeps_sources_distinct() -> None:
    stack = StyleStack()
    stack.add(StyleLayer(StyleSourceKind.STYLE_DNA, value=StyleDNA(name="house-style")))
    stack.add(StyleLayer(StyleSourceKind.PROVIDER_PRESET, name="Design", provider="ideogram"))
    stack.add(StyleLayer(StyleSourceKind.CUSTOM_MODEL, name="brand-model", provider="ideogram"))
    assert [item.source_kind for item in stack.layers] == [
        StyleSourceKind.STYLE_DNA,
        StyleSourceKind.PROVIDER_PRESET,
        StyleSourceKind.CUSTOM_MODEL,
    ]


def test_recovered_prompt_imports_to_scene_graph() -> None:
    expanded = {
        "high_level_description": "Poster with a large title and moon",
        "compositional_deconstruction": {
            "background": "dark blue night sky",
            "elements": [
                {"type": "text", "text": "NOCTURNE", "desc": "large centered title"},
                {"type": "obj", "desc": "crescent moon in upper right"},
            ],
        },
    }
    manifest = prompt_manifest_from_decomposition(
        "prompt-1",
        decompose_prompt("make a moon poster", expanded),
    )
    assert manifest.original_prompt == "make a moon poster"
    assert manifest.scene is not None
    assert manifest.scene.elements[0].kind is SceneElementKind.TEXT
    assert manifest.scene.elements[0].text == "NOCTURNE"
    assert manifest.scene.elements[1].kind is SceneElementKind.OBJECT


def test_mock_backend_is_repeatable() -> None:
    backend = DeterministicMockBackend()
    request = OperationRequest(OperationKind.GENERATE, prompt_manifest_id="prompt-1")
    first = backend.execute(request)
    second = backend.execute(request)
    assert first.job_id == second.job_id
    assert first.outputs == second.outputs
    assert first.execution_mode is ExecutionMode.MOCK
    assert first.provider_call_performed is False
    registry = ProviderRegistry()
    registry.register(backend)
    assert registry.names() == ["mock"]
    assert registry.supporting(OperationKind.REMIX) == [backend]
