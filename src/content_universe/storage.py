from __future__ import annotations

import json
import sqlite3
from pathlib import Path
from typing import Iterable

from .catalog import GenerationRecord
from .graph import CreativeGraph
from .models import AssetRecord, CollectionRecord, CreativeEntity, ProfileRecord
from .provenance import ProvenanceLedger


SCHEMA = """
PRAGMA journal_mode=WAL;
CREATE TABLE IF NOT EXISTS generations (
  request_id TEXT PRIMARY KEY,
  request_type TEXT,
  model_version TEXT,
  created REAL,
  payload_json TEXT NOT NULL
);
CREATE TABLE IF NOT EXISTS responses (
  response_id TEXT PRIMARY KEY,
  request_id TEXT NOT NULL,
  response_index INTEGER,
  payload_json TEXT NOT NULL,
  FOREIGN KEY(request_id) REFERENCES generations(request_id)
);
CREATE TABLE IF NOT EXISTS assets (
  asset_id TEXT PRIMARY KEY,
  response_id TEXT,
  url TEXT,
  representation TEXT,
  resolution TEXT,
  payload_json TEXT NOT NULL
);
CREATE TABLE IF NOT EXISTS collections (
  collection_id TEXT PRIMARY KEY,
  collection_type TEXT,
  version_id TEXT,
  payload_json TEXT NOT NULL
);
CREATE TABLE IF NOT EXISTS profiles (
  profile_key TEXT PRIMARY KEY,
  user_id TEXT,
  handle TEXT,
  payload_json TEXT NOT NULL
);
CREATE TABLE IF NOT EXISTS creative_entities (
  entity_key TEXT PRIMARY KEY,
  entity_id TEXT NOT NULL,
  kind TEXT NOT NULL,
  title TEXT,
  payload_json TEXT NOT NULL
);
CREATE TABLE IF NOT EXISTS graph_edges (
  source TEXT NOT NULL,
  target TEXT NOT NULL,
  kind TEXT NOT NULL,
  edge_id TEXT NOT NULL DEFAULT '',
  metadata_json TEXT NOT NULL,
  PRIMARY KEY(source, target, kind, edge_id)
);
CREATE TABLE IF NOT EXISTS provenance (
  entity_key TEXT NOT NULL,
  source TEXT NOT NULL,
  observed_at TEXT NOT NULL,
  locator TEXT NOT NULL DEFAULT '',
  confidence REAL,
  metadata_json TEXT NOT NULL,
  PRIMARY KEY(entity_key, source, observed_at, locator)
);
CREATE TABLE IF NOT EXISTS universe_metadata (
  key TEXT PRIMARY KEY,
  value_json TEXT NOT NULL
);
CREATE INDEX IF NOT EXISTS idx_generations_model ON generations(model_version);
CREATE INDEX IF NOT EXISTS idx_generations_created ON generations(created);
CREATE INDEX IF NOT EXISTS idx_responses_request ON responses(request_id);
CREATE INDEX IF NOT EXISTS idx_assets_response ON assets(response_id);
CREATE INDEX IF NOT EXISTS idx_profiles_handle ON profiles(handle);
CREATE INDEX IF NOT EXISTS idx_creative_entities_kind ON creative_entities(kind);
CREATE INDEX IF NOT EXISTS idx_creative_entities_title ON creative_entities(title);
CREATE INDEX IF NOT EXISTS idx_edges_source ON graph_edges(source);
CREATE INDEX IF NOT EXISTS idx_edges_target ON graph_edges(target);
CREATE INDEX IF NOT EXISTS idx_provenance_entity ON provenance(entity_key);
"""


class SQLiteStore:
    def __init__(self, path: str | Path) -> None:
        self.path = Path(path)
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self.db = sqlite3.connect(self.path)
        self.db.execute("PRAGMA foreign_keys=ON")
        self.db.executescript(SCHEMA)
        self._migrate_graph_edge_identity()

    def _migrate_graph_edge_identity(self) -> None:
        """Upgrade pre-CreativeOS graph tables without losing existing edges."""

        columns = {
            str(row[1])
            for row in self.db.execute("PRAGMA table_info(graph_edges)").fetchall()
        }
        if "edge_id" in columns:
            return

        with self.db:
            self.db.execute("ALTER TABLE graph_edges RENAME TO graph_edges_legacy")
            self.db.execute(
                """
                CREATE TABLE graph_edges (
                  source TEXT NOT NULL,
                  target TEXT NOT NULL,
                  kind TEXT NOT NULL,
                  edge_id TEXT NOT NULL DEFAULT '',
                  metadata_json TEXT NOT NULL,
                  PRIMARY KEY(source, target, kind, edge_id)
                )
                """
            )
            self.db.execute(
                """
                INSERT INTO graph_edges(source,target,kind,edge_id,metadata_json)
                SELECT source,target,kind,'',metadata_json FROM graph_edges_legacy
                """
            )
            self.db.execute("DROP TABLE graph_edges_legacy")
            self.db.execute("CREATE INDEX IF NOT EXISTS idx_edges_source ON graph_edges(source)")
            self.db.execute("CREATE INDEX IF NOT EXISTS idx_edges_target ON graph_edges(target)")

    def close(self) -> None:
        self.db.close()

    def __enter__(self) -> "SQLiteStore":
        return self

    def __exit__(self, *_: object) -> None:
        self.close()

    def upsert_generation(self, record: GenerationRecord) -> None:
        payload = record.to_dict()
        self.db.execute(
            "INSERT INTO generations(request_id, request_type, model_version, created, payload_json) VALUES(?,?,?,?,?) "
            "ON CONFLICT(request_id) DO UPDATE SET request_type=excluded.request_type, model_version=excluded.model_version, created=excluded.created, payload_json=excluded.payload_json",
            (record.request_id, record.request_type, record.model_version, record.creation_time_float, json.dumps(payload, ensure_ascii=False)),
        )
        for response in record.responses.values():
            self.db.execute(
                "INSERT INTO responses(response_id, request_id, response_index, payload_json) VALUES(?,?,?,?) "
                "ON CONFLICT(response_id) DO UPDATE SET request_id=excluded.request_id, response_index=excluded.response_index, payload_json=excluded.payload_json",
                (response.response_id, record.request_id, response.response_index, json.dumps(response.to_dict(), ensure_ascii=False)),
            )

    def upsert_many(self, records: Iterable[GenerationRecord]) -> None:
        with self.db:
            for record in records:
                self.upsert_generation(record)

    def upsert_asset(self, record: AssetRecord) -> None:
        self.db.execute(
            "INSERT INTO assets(asset_id,response_id,url,representation,resolution,payload_json) VALUES(?,?,?,?,?,?) "
            "ON CONFLICT(asset_id) DO UPDATE SET response_id=excluded.response_id,url=excluded.url,representation=excluded.representation,resolution=excluded.resolution,payload_json=excluded.payload_json",
            (record.asset_id, record.response_id, record.url, record.representation, record.resolution, json.dumps(record.to_dict(), ensure_ascii=False)),
        )

    def upsert_collection(self, record: CollectionRecord) -> None:
        self.db.execute(
            "INSERT INTO collections(collection_id,collection_type,version_id,payload_json) VALUES(?,?,?,?) "
            "ON CONFLICT(collection_id) DO UPDATE SET collection_type=excluded.collection_type,version_id=excluded.version_id,payload_json=excluded.payload_json",
            (record.collection_id, record.collection_type, record.version_id, json.dumps(record.to_dict(), ensure_ascii=False)),
        )

    def upsert_profile(self, record: ProfileRecord) -> None:
        key = record.user_id or record.handle
        if not key:
            raise ValueError("profile requires user_id or handle")
        self.db.execute(
            "INSERT INTO profiles(profile_key,user_id,handle,payload_json) VALUES(?,?,?,?) "
            "ON CONFLICT(profile_key) DO UPDATE SET user_id=excluded.user_id,handle=excluded.handle,payload_json=excluded.payload_json",
            (key, record.user_id, record.handle, json.dumps(record.to_dict(), ensure_ascii=False)),
        )

    def upsert_entity(self, record: CreativeEntity) -> None:
        self.db.execute(
            "INSERT INTO creative_entities(entity_key,entity_id,kind,title,payload_json) VALUES(?,?,?,?,?) "
            "ON CONFLICT(entity_key) DO UPDATE SET entity_id=excluded.entity_id,kind=excluded.kind,title=excluded.title,payload_json=excluded.payload_json",
            (record.ref.key, record.entity_id, record.kind.value, record.title, json.dumps(record.to_dict(), ensure_ascii=False)),
        )

    def save_graph(self, graph: CreativeGraph) -> None:
        with self.db:
            for edge in graph.edges:
                self.db.execute(
                    "INSERT OR REPLACE INTO graph_edges(source,target,kind,edge_id,metadata_json) VALUES(?,?,?,?,?)",
                    (
                        edge.source.key,
                        edge.target.key,
                        edge.kind.value,
                        edge.edge_id or "",
                        json.dumps(edge.metadata, ensure_ascii=False),
                    ),
                )

    def save_provenance(self, ledger: ProvenanceLedger) -> None:
        with self.db:
            for key, observations in ledger.observations.items():
                for item in observations:
                    self.db.execute(
                        "INSERT OR REPLACE INTO provenance(entity_key,source,observed_at,locator,confidence,metadata_json) VALUES(?,?,?,?,?,?)",
                        (key, item.source, item.observed_at, item.locator or "", item.confidence, json.dumps(item.metadata, ensure_ascii=False)),
                    )

    def save_metadata(self, metadata: dict) -> None:
        with self.db:
            for key, value in metadata.items():
                self.db.execute(
                    "INSERT OR REPLACE INTO universe_metadata(key,value_json) VALUES(?,?)",
                    (str(key), json.dumps(value, ensure_ascii=False)),
                )

    def save_universe(self, universe) -> None:
        """Persist a ContentUniverse without importing it at module import time."""
        with self.db:
            for record in universe.generations.values():
                self.upsert_generation(record)
            for record in universe.assets.values():
                self.upsert_asset(record)
            for record in universe.collections.values():
                self.upsert_collection(record)
            for record in universe.profiles.values():
                self.upsert_profile(record)
            for record in universe.entities.values():
                self.upsert_entity(record)
        self.save_graph(universe.graph)
        self.save_provenance(universe.provenance)
        self.save_metadata(universe.metadata)

    def stats(self) -> dict[str, int]:
        def count(table: str) -> int:
            return int(self.db.execute(f"SELECT COUNT(*) FROM {table}").fetchone()[0])

        return {
            "generations": count("generations"),
            "responses": count("responses"),
            "assets": count("assets"),
            "collections": count("collections"),
            "profiles": count("profiles"),
            "creative_entities": count("creative_entities"),
            "graph_edges": count("graph_edges"),
            "provenance": count("provenance"),
        }
