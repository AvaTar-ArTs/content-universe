import pytest

from content_universe.creativeos import (
    BoundingBox,
    IdeogramJsonDialect,
    OperationKind,
    PromptBuilder,
    ProviderOperationRequired,
    ReferenceBinding,
    ReferenceKind,
    ReferenceRole,
    SceneElement,
    SceneElementKind,
)
from content_universe.models import EntityKind, EntityRef


def test_ideogram_json_round_trip_preserves_structure_and_original_prompt() -> None:
    dialect = IdeogramJsonDialect()
    builder = PromptBuilder()
    payload = {
        "user_prompt": "make a moon poster",
        "prompt": {
            "high_level_description": "Poster with title and crescent moon",
            "compositional_deconstruction": {
                "background": "night sky",
                "elements": [
                    {"type": "text", "text": "NOCTURNE", "desc": "large centered title", "custom": 7},
                    {"type": "obj", "desc": "crescent moon upper right"},
                ],
            },
        },
    }

    manifest = builder.import_payload(dialect, payload, manifest_id="poster-1")
    exported = builder.export(manifest, dialect)

    assert manifest.original_prompt == "make a moon poster"
    assert manifest.scene is not None
    assert manifest.scene.elements[0].kind is SceneElementKind.TEXT
    assert exported["structured_prompt"]["compositional_deconstruction"]["elements"][0]["custom"] == 7
    assert exported["structured_prompt"]["compositional_deconstruction"]["elements"][0]["text"] == "NOCTURNE"


def test_prompt_builder_local_composition_and_localization() -> None:
    builder = PromptBuilder()
    manifest = builder.build("poster-2", prompt="make a poster")
    builder.compose_add(
        manifest,
        SceneElement("headline", SceneElementKind.TEXT, text="HELLO"),
    )
    builder.compose_move(manifest, "headline", BoundingBox(0.1, 0.1, 0.8, 0.2))
    builder.localize(manifest, {"HELLO": "BONJOUR"}, language="fr")
    builder.reflow(manifest, aspect_ratio="9:16")

    assert manifest.scene is not None
    assert manifest.scene.get_element("headline").text == "BONJOUR"
    assert manifest.aspect_ratio == "9:16"
    assert manifest.lineage is not None
    assert manifest.lineage.original == "make a poster"


def test_provider_methods_do_not_fake_results() -> None:
    builder = PromptBuilder()
    manifest = builder.build("poster-3", prompt="rough prompt")
    source = EntityRef(EntityKind.ASSET, "asset-1")

    with pytest.raises(ProviderOperationRequired) as describe:
        builder.describe(source)
    assert describe.value.operation is OperationKind.DESCRIBE

    with pytest.raises(ProviderOperationRequired) as magic:
        builder.magic_prompt(manifest)
    assert magic.value.operation is OperationKind.MAGIC_PROMPT

    with pytest.raises(ProviderOperationRequired) as layerize:
        builder.layerize_text(source)
    assert layerize.value.operation is OperationKind.LAYERIZE_TEXT


def test_reference_generation_flag_is_derived_from_role() -> None:
    authoring = ReferenceBinding(
        role=ReferenceRole.AUTHORING,
        kind=ReferenceKind.COMPOSITION,
        locator="canvas://layout-1",
    )
    generation = ReferenceBinding(
        role=ReferenceRole.GENERATION,
        kind=ReferenceKind.CHARACTER,
        locator="character://hero",
    )
    assert authoring.passed_to_generation is False
    assert generation.passed_to_generation is True
    assert authoring.to_dict()["passed_to_generation"] is False


def test_ideogram_dialect_requires_exact_text_for_text_element() -> None:
    builder = PromptBuilder()
    manifest = builder.build("poster-4", prompt="poster")
    builder.compose_add(manifest, SceneElement("headline", SceneElementKind.TEXT))
    report = builder.validate(manifest, IdeogramJsonDialect())
    assert report.valid is False
    assert "exact text" in report.errors[0]
