from __future__ import annotations

from typing import Any, Iterable

from ...catalog import GenerationRecord
from ...graph import GraphEdge
from ...models import AssetRecord, CollectionRecord, EdgeKind, EntityKind, EntityRef
from ...provenance import Observation
from ...universe import ContentUniverse

BRANCH_EDGE = {
    "style": EdgeKind.STYLE_REFERENCE,
    "character": EdgeKind.CHARACTER_REFERENCE,
    "product": EdgeKind.PRODUCT_REFERENCE,
    "edit": EdgeKind.EDIT_OF,
    "variation": EdgeKind.VARIATION_OF,
    "upload": EdgeKind.UPLOAD_PARENT,
}


def _walk_reference_nodes(value: Any, branch: str | None = None) -> Iterable[tuple[str | None, dict[str, Any]]]:
    if isinstance(value, dict):
        yield branch, value
        for key, child in value.items():
            child_branch = key if key in BRANCH_EDGE else branch
            yield from _walk_reference_nodes(child, child_branch)
    elif isinstance(value, list):
        for child in value:
            yield from _walk_reference_nodes(child, branch)


def _asset_identifiers(node: dict[str, Any]) -> list[dict[str, Any]]:
    value = node.get("asset_identifiers")
    if isinstance(value, list):
        return [item for item in value if isinstance(item, dict)]
    return []


def enrich_reference_entities(universe: ContentUniverse, record: GenerationRecord) -> None:
    request_ref = EntityRef(EntityKind.GENERATION, record.request_id)

    explicit_collections = (
        ("style", record.style_reference_collection_ids),
        ("character", record.character_reference_collection_ids),
        ("product", record.product_reference_collection_ids),
    )
    for collection_type, ids in explicit_collections:
        for collection_id in ids:
            collection = universe.ingest_collection(CollectionRecord(
                collection_id=collection_id,
                collection_type=collection_type,
                sources=list(record.sources),
            ))
            collection_ref = EntityRef(EntityKind.COLLECTION, collection.collection_id)
            universe.graph.add(GraphEdge(request_ref, collection_ref, BRANCH_EDGE[collection_type]))
            for source in record.sources:
                universe.provenance.add(collection_ref.key, Observation(source=source))

    for branch, node in _walk_reference_nodes(record.references or {}):
        collection_id = node.get("reference_collection_id") or node.get("collection_id")
        version_id = node.get("reference_collection_version_id") or node.get("collection_version_id")
        assets = _asset_identifiers(node)

        collection: CollectionRecord | None = None
        if collection_id:
            collection = universe.ingest_collection(CollectionRecord(
                collection_id=str(collection_id),
                collection_type=branch,
                version_id=str(version_id) if version_id else None,
                assets=[str(item["asset_id"]) for item in assets if item.get("asset_id")],
                metadata={"reference_node": node},
                sources=list(record.sources),
            ))
            collection_ref = EntityRef(EntityKind.COLLECTION, collection.collection_id)
            universe.graph.add(GraphEdge(request_ref, collection_ref, BRANCH_EDGE.get(branch or "", EdgeKind.RELATED_TO)))

        for item in assets:
            asset_id = item.get("asset_id")
            if not asset_id:
                continue
            asset = universe.ingest_asset(AssetRecord(
                asset_id=str(asset_id),
                representation=(item.get("metadata") or {}).get("representation") if isinstance(item.get("metadata"), dict) else None,
                metadata={"asset_type": item.get("asset_type"), "reference_identifier": item},
                sources=list(record.sources),
            ))
            asset_ref = EntityRef(EntityKind.ASSET, asset.asset_id)
            if collection is not None:
                universe.graph.add(GraphEdge(asset_ref, EntityRef(EntityKind.COLLECTION, collection.collection_id), EdgeKind.MEMBER_OF))
            else:
                universe.graph.add(GraphEdge(request_ref, asset_ref, BRANCH_EDGE.get(branch or "", EdgeKind.RELATED_TO)))
            for source in record.sources:
                universe.provenance.add(asset_ref.key, Observation(source=source))


def enrich_all_references(universe: ContentUniverse) -> None:
    for record in universe.generations.values():
        enrich_reference_entities(universe, record)
