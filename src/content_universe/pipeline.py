from __future__ import annotations

from pathlib import Path
from typing import Iterable
from urllib.parse import urlparse

from .adapters import default_registry
from .adapters.base import AdapterRegistry
from .adapters.ideogram.assets import parse_asset_url
from .adapters.ideogram.references import enrich_all_references
from .graph import GraphEdge
from .lineage import graph_from_records
from .models import AssetRecord, EdgeKind, EntityKind, EntityRef
from .provenance import Observation
from .universe import ContentUniverse


def merge_universes(target: ContentUniverse, incoming: ContentUniverse) -> ContentUniverse:
    for record in incoming.generations.values():
        target.ingest_generation(record)
    for record in incoming.assets.values():
        target.ingest_asset(record)
    for record in incoming.collections.values():
        target.ingest_collection(record)
    for record in incoming.profiles.values():
        target.ingest_profile(record)
    for record in incoming.entities.values():
        target.ingest_entity(record)
    target.graph.extend(incoming.graph.edges)
    for key, observations in incoming.provenance.observations.items():
        for observation in observations:
            target.provenance.add(key, observation)
    target.metadata.update(incoming.metadata)
    target.warnings.extend(incoming.warnings)
    return target


def derive_primary_assets(universe: ContentUniverse) -> None:
    """Create canonical primary AssetRecords for response asset URLs.

    Ideogram URLs expose representation/resolution directly. Other platforms get
    a conservative `primary` composite asset ID without pretending the URL is a
    platform-native asset identifier.
    """
    for generation in universe.generations.values():
        for response in generation.responses.values():
            if not response.asset_url:
                continue
            parsed_url = urlparse(response.asset_url)
            representation = "primary"
            resolution = None
            if parsed_url.hostname in {"ideogram.ai", "www.ideogram.ai"}:
                parsed = parse_asset_url(response.asset_url)
                representation = parsed.get("representation") or representation
                resolution = parsed.get("resolution")
            asset_id = f"{response.response_id}:{representation}:{resolution or 'native'}"
            asset = AssetRecord(
                asset_id=asset_id,
                response_id=response.response_id,
                url=response.asset_url,
                representation=representation,
                resolution=resolution,
                sources=list(response.sources),
            )
            universe.ingest_asset(asset)
            response_ref = EntityRef(EntityKind.RESPONSE, response.response_id)
            asset_ref = EntityRef(EntityKind.ASSET, asset_id)
            universe.graph.add(GraphEdge(response_ref, asset_ref, EdgeKind.PRODUCED))
            for source in response.sources:
                universe.provenance.add(asset_ref.key, Observation(source=source, locator=response.asset_url))


def finalize_universe(universe: ContentUniverse) -> ContentUniverse:
    universe.graph.extend(graph_from_records(universe.generations.values()).edges)
    derive_primary_assets(universe)
    enrich_all_references(universe)
    return universe


def harvest_sources(
    sources: Iterable[str | Path],
    *,
    registry: AdapterRegistry | None = None,
    ignore_unsupported: bool = False,
) -> ContentUniverse:
    registry = registry or default_registry()
    universe = ContentUniverse()

    for source in sources:
        try:
            result = registry.harvest(source)
        except ValueError as exc:
            if not ignore_unsupported:
                raise
            universe.warnings.append(str(exc))
            continue
        universe.ingest_harvest(result)

    return finalize_universe(universe)
