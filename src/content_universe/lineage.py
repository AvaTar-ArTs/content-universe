from __future__ import annotations

from typing import Any, Iterable

from .catalog import GenerationRecord
from .graph import CreativeGraph, GraphEdge
from .models import EdgeKind, EntityKind, EntityRef


def _asset_ids(value: Any) -> Iterable[tuple[str, dict[str, Any]]]:
    if isinstance(value, dict):
        if value.get("asset_id"):
            yield str(value["asset_id"]), value
        for child in value.values():
            yield from _asset_ids(child)
    elif isinstance(value, list):
        for child in value:
            yield from _asset_ids(child)


def graph_from_generation(record: GenerationRecord) -> CreativeGraph:
    """Build conservative lineage edges from a normalized generation record.

    The function only creates relationships supported by identifiers present in
    the captured record. It does not guess whether an arbitrary referenced
    response was an edit, remix, or style source unless the reference branch
    gives that relationship a name.
    """
    graph = CreativeGraph()
    req = EntityRef(EntityKind.GENERATION, record.request_id)

    for response in record.responses.values():
        graph.add(GraphEdge(req, EntityRef(EntityKind.RESPONSE, response.response_id), EdgeKind.PRODUCED, {"response_index": response.response_index}))

    branch_map = {
        "edit": EdgeKind.EDIT_OF,
        "variation": EdgeKind.VARIATION_OF,
        "style": EdgeKind.STYLE_REFERENCE,
        "character": EdgeKind.CHARACTER_REFERENCE,
        "product": EdgeKind.PRODUCT_REFERENCE,
        "upload": EdgeKind.UPLOAD_PARENT,
    }

    references = record.references or {}
    for branch, kind in branch_map.items():
        value = references.get(branch)
        if not value:
            continue
        for asset_id, raw in _asset_ids(value):
            graph.add(GraphEdge(req, EntityRef(EntityKind.ASSET, asset_id), kind, {"evidence": raw}))

    for collection_id in record.style_reference_collection_ids:
        graph.add(GraphEdge(req, EntityRef(EntityKind.COLLECTION, collection_id), EdgeKind.STYLE_REFERENCE))
    for collection_id in record.character_reference_collection_ids:
        graph.add(GraphEdge(req, EntityRef(EntityKind.COLLECTION, collection_id), EdgeKind.CHARACTER_REFERENCE))
    for collection_id in record.product_reference_collection_ids:
        graph.add(GraphEdge(req, EntityRef(EntityKind.COLLECTION, collection_id), EdgeKind.PRODUCT_REFERENCE))

    return graph


def graph_from_records(records: Iterable[GenerationRecord]) -> CreativeGraph:
    graph = CreativeGraph()
    for record in records:
        graph.extend(graph_from_generation(record).edges)
    return graph
