from __future__ import annotations

import json
import tomllib
from pathlib import Path
from typing import Any

from .graph import GraphEdge
from .models import CreativeEntity, EdgeKind, EntityKind, EntityRef
from .provenance import Observation
from .universe import ContentUniverse


def parse_entity_ref(value: str) -> EntityRef:
    kind_text, sep, entity_id = value.partition(":")
    if not sep or not entity_id:
        raise ValueError(f"entity reference must look like kind:id, got {value!r}")
    return EntityRef(EntityKind(kind_text), entity_id)


def load_manifest_payload(path: str | Path) -> dict[str, Any]:
    manifest_path = Path(path)
    if manifest_path.suffix.lower() == ".toml":
        with manifest_path.open("rb") as handle:
            return tomllib.load(handle)
    if manifest_path.suffix.lower() == ".json":
        return json.loads(manifest_path.read_text(encoding="utf-8"))
    raise ValueError("Content Universe manifests must be .toml or .json")


def universe_from_manifest(path: str | Path) -> ContentUniverse:
    manifest_path = Path(path)
    payload = load_manifest_payload(manifest_path)
    universe = ContentUniverse(metadata=dict(payload.get("universe") or {}))
    source = f"manifest:{manifest_path.name}"

    for item in payload.get("entities") or []:
        if not isinstance(item, dict):
            continue
        entity = CreativeEntity(
            entity_id=str(item["id"]),
            kind=EntityKind(str(item["kind"])),
            title=item.get("title"),
            description=item.get("description"),
            aliases=[str(v) for v in item.get("aliases") or []],
            tags=[str(v) for v in item.get("tags") or []],
            metadata=dict(item.get("metadata") or {}),
            sources=[source],
        )
        universe.ingest_entity(entity)
        universe.provenance.add(entity.ref.key, Observation(source=source, locator=str(manifest_path)))

    for item in payload.get("relationships") or []:
        if not isinstance(item, dict):
            continue
        source_ref = parse_entity_ref(str(item["source"]))
        target_ref = parse_entity_ref(str(item["target"]))
        universe.graph.add(GraphEdge(
            source=source_ref,
            target=target_ref,
            kind=EdgeKind(str(item["kind"])),
            metadata=dict(item.get("metadata") or {}),
        ))

    return universe


def manifest_template() -> str:
    return '''[universe]\nname = "My Content Universe"\n\n[[entities]]\nid = "series-id"\nkind = "series"\ntitle = "Series Title"\ntags = ["manga", "music"]\n\n[[entities]]\nid = "hero-id"\nkind = "character"\ntitle = "Hero"\n\n[[relationships]]\nsource = "series:series-id"\nkind = "features"\ntarget = "character:hero-id"\n'''
