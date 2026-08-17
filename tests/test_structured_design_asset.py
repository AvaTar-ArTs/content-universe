from content_universe.creativeos import (
    BoundingBox,
    GenerationWindow,
    Mask,
    StructuredDesignAsset,
    persist_structured_design_asset,
)
from content_universe.models import EdgeKind, EntityKind, EntityRef
from content_universe.universe import ContentUniverse


def test_structured_design_asset_persists_editable_structure_and_lineage() -> None:
    universe = ContentUniverse()
    design = StructuredDesignAsset(
        design_id="cover-v2",
        base_asset=EntityRef(EntityKind.ASSET, "cover-raster"),
        scene_graph_id="cover-scene",
        prompt_manifest_id="cover-prompt",
        style_dna_ids=["house-style"],
        vector_assets=[EntityRef(EntityKind.ASSET, "logo-svg")],
        masks=[Mask("title-mask", bounds=BoundingBox(0.1, 0.1, 0.8, 0.2), purpose="title replacement")],
        generation_windows=[
            GenerationWindow(
                "hero-window",
                BoundingBox(0.2, 0.25, 0.6, 0.6),
                element_ids=["hero"],
                locked_element_ids=["headline"],
                operation_hint="edit",
            )
        ],
        parent_design=EntityRef(EntityKind.STRUCTURED_DESIGN_ASSET, "cover-v1"),
    )

    entity = persist_structured_design_asset(universe, design)
    assert entity.kind is EntityKind.STRUCTURED_DESIGN_ASSET
    assert any(edge.kind is EdgeKind.RENDERED_AS for edge in universe.graph.edges)
    assert any(edge.kind is EdgeKind.DERIVED_FROM for edge in universe.graph.edges)
    roles = {edge.metadata.get("role") for edge in universe.graph.edges if edge.kind is EdgeKind.USES}
    assert {"base_asset", "scene_graph", "style_dna", "vector_asset"}.issubset(roles)
