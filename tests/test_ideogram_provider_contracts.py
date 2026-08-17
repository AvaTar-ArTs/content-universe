from content_universe.creativeos.operations import OperationKind
from content_universe.providers.ideogram import IDEOGRAM_TOOL_CATALOG


def test_ideogram_catalog_preserves_historical_26_tool_surface() -> None:
    assert len(IDEOGRAM_TOOL_CATALOG) == 26
    assert IDEOGRAM_TOOL_CATALOG.get("generate_image").family == "creation"
    assert IDEOGRAM_TOOL_CATALOG.get("train_model").family == "training"
    assert IDEOGRAM_TOOL_CATALOG.get("list_organizations").mutating is False


def test_provider_transforms_map_to_semantic_operations() -> None:
    assert IDEOGRAM_TOOL_CATALOG.get("edit_image").semantic_operation is OperationKind.EDIT
    assert IDEOGRAM_TOOL_CATALOG.get("remix_image").semantic_operation is OperationKind.REMIX
    assert IDEOGRAM_TOOL_CATALOG.get("reframe_image").semantic_operation is OperationKind.REFRAME
    assert IDEOGRAM_TOOL_CATALOG.get("upscale_image").semantic_operation is OperationKind.UPSCALE


def test_destructive_collection_contracts_remain_explicit() -> None:
    destructive = {tool.name for tool in IDEOGRAM_TOOL_CATALOG.destructive()}
    assert destructive == {"delete_collection", "remove_images_from_collection"}
