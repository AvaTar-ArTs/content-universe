from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from .adapters.base import HarvestResult
from .catalog import Catalog, GenerationRecord
from .graph import CreativeGraph
from .models import AssetRecord, CollectionRecord, CreativeEntity, ProfileRecord
from .provenance import ProvenanceLedger


def _merge_dict(old: dict[str, Any], new: dict[str, Any]) -> dict[str, Any]:
    result = dict(old)
    for key, value in new.items():
        if value not in (None, "", [], {}):
            result[key] = value
    return result


@dataclass(slots=True)
class ContentUniverse:
    catalog: Catalog = field(default_factory=Catalog)
    assets: dict[str, AssetRecord] = field(default_factory=dict)
    collections: dict[str, CollectionRecord] = field(default_factory=dict)
    profiles: dict[str, ProfileRecord] = field(default_factory=dict)
    entities: dict[str, CreativeEntity] = field(default_factory=dict)
    graph: CreativeGraph = field(default_factory=CreativeGraph)
    provenance: ProvenanceLedger = field(default_factory=ProvenanceLedger)
    metadata: dict[str, Any] = field(default_factory=dict)
    warnings: list[str] = field(default_factory=list)

    @property
    def generations(self) -> dict[str, GenerationRecord]:
        return self.catalog.generations

    def ingest_generation(self, record: GenerationRecord) -> GenerationRecord:
        return self.catalog.ingest(record)

    def ingest_asset(self, record: AssetRecord) -> AssetRecord:
        existing = self.assets.get(record.asset_id)
        if existing is None:
            self.assets[record.asset_id] = record
            return record
        existing.response_id = record.response_id or existing.response_id
        existing.url = record.url or existing.url
        existing.representation = record.representation or existing.representation
        existing.resolution = record.resolution or existing.resolution
        existing.media_type = record.media_type or existing.media_type
        existing.width = record.width or existing.width
        existing.height = record.height or existing.height
        existing.metadata = _merge_dict(existing.metadata, record.metadata)
        existing.sources = list(dict.fromkeys(existing.sources + record.sources))
        return existing

    def ingest_collection(self, record: CollectionRecord) -> CollectionRecord:
        existing = self.collections.get(record.collection_id)
        if existing is None:
            self.collections[record.collection_id] = record
            return record
        existing.collection_type = record.collection_type or existing.collection_type
        existing.version_id = record.version_id or existing.version_id
        existing.assets = list(dict.fromkeys(existing.assets + record.assets))
        existing.metadata = _merge_dict(existing.metadata, record.metadata)
        existing.sources = list(dict.fromkeys(existing.sources + record.sources))
        return existing

    def ingest_profile(self, record: ProfileRecord) -> ProfileRecord:
        key = record.user_id or record.handle
        if not key:
            raise ValueError("profile requires user_id or handle")
        existing = self.profiles.get(key)
        if existing is None:
            self.profiles[key] = record
            return record
        existing.user_id = record.user_id or existing.user_id
        existing.handle = record.handle or existing.handle
        existing.generation_count = record.generation_count if record.generation_count is not None else existing.generation_count
        existing.likes = record.likes if record.likes is not None else existing.likes
        existing.joined_at = record.joined_at or existing.joined_at
        existing.metadata = _merge_dict(existing.metadata, record.metadata)
        existing.sources = list(dict.fromkeys(existing.sources + record.sources))
        return existing

    def ingest_entity(self, record: CreativeEntity) -> CreativeEntity:
        key = record.ref.key
        existing = self.entities.get(key)
        if existing is None:
            self.entities[key] = record
            return record
        existing.title = record.title or existing.title
        existing.description = record.description or existing.description
        existing.aliases = list(dict.fromkeys(existing.aliases + record.aliases))
        existing.tags = list(dict.fromkeys(existing.tags + record.tags))
        existing.metadata = _merge_dict(existing.metadata, record.metadata)
        existing.sources = list(dict.fromkeys(existing.sources + record.sources))
        return existing

    def ingest_harvest(self, result: HarvestResult) -> None:
        self.catalog.extend(result.records)
        self.graph.extend(result.graph.edges)
        for key, observations in result.provenance.observations.items():
            for observation in observations:
                self.provenance.add(key, observation)
        self.metadata.update(result.metadata)
        self.warnings.extend(result.warnings)

    def summary(self) -> dict[str, Any]:
        entity_kinds: dict[str, int] = {}
        for entity in self.entities.values():
            entity_kinds[entity.kind.value] = entity_kinds.get(entity.kind.value, 0) + 1
        return {
            **self.catalog.summary(),
            "asset_count": len(self.assets),
            "collection_count": len(self.collections),
            "profile_count": len(self.profiles),
            "creative_entity_count": len(self.entities),
            "creative_entity_kinds": dict(sorted(entity_kinds.items())),
            "graph_edge_count": len(self.graph.edges),
            "provenance_entity_count": len(self.provenance.observations),
            "warning_count": len(self.warnings),
        }

    def to_dict(self) -> dict[str, Any]:
        return {
            "summary": self.summary(),
            "generations": [record.to_dict() for record in self.generations.values()],
            "assets": [record.to_dict() for record in self.assets.values()],
            "collections": [record.to_dict() for record in self.collections.values()],
            "profiles": [record.to_dict() for record in self.profiles.values()],
            "entities": [record.to_dict() for record in self.entities.values()],
            "graph": self.graph.to_dict(),
            "provenance": self.provenance.to_dict(),
            "metadata": self.metadata,
            "warnings": self.warnings,
        }
