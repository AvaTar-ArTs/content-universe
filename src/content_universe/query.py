from __future__ import annotations

import json
import sqlite3
from pathlib import Path
from typing import Any

from .fts import fts_available


class CatalogQuery:
    def __init__(self, path: str | Path) -> None:
        self.path = Path(path)

    def _connect(self) -> sqlite3.Connection:
        db = sqlite3.connect(self.path)
        db.row_factory = sqlite3.Row
        return db

    def _payload(self, table: str, key_column: str, key: str) -> dict[str, Any] | None:
        with self._connect() as db:
            row = db.execute(f"SELECT payload_json FROM {table} WHERE {key_column}=?", (key,)).fetchone()
        return json.loads(row[0]) if row else None

    def generation(self, request_id: str) -> dict[str, Any] | None:
        return self._payload("generations", "request_id", request_id)

    def response(self, response_id: str) -> dict[str, Any] | None:
        return self._payload("responses", "response_id", response_id)

    def asset(self, asset_id: str) -> dict[str, Any] | None:
        return self._payload("assets", "asset_id", asset_id)

    def collection(self, collection_id: str) -> dict[str, Any] | None:
        return self._payload("collections", "collection_id", collection_id)

    def creative_entity(self, entity_key: str) -> dict[str, Any] | None:
        return self._payload("creative_entities", "entity_key", entity_key)

    def profile(self, key_or_handle: str) -> dict[str, Any] | None:
        with self._connect() as db:
            row = db.execute(
                "SELECT payload_json FROM profiles WHERE profile_key=? OR handle=? LIMIT 1",
                (key_or_handle, key_or_handle),
            ).fetchone()
        return json.loads(row[0]) if row else None

    def search_prompts(self, text: str, limit: int = 20) -> list[dict[str, Any]]:
        with self._connect() as db:
            if fts_available(db):
                try:
                    rows = db.execute(
                        "SELECT g.payload_json FROM generation_fts f JOIN generations g ON g.request_id=f.request_id WHERE generation_fts MATCH ? ORDER BY bm25(generation_fts) LIMIT ?",
                        (text, limit),
                    ).fetchall()
                    return [json.loads(row[0]) for row in rows]
                except sqlite3.OperationalError:
                    pass
            needle = f"%{text}%"
            rows = db.execute(
                "SELECT payload_json FROM generations WHERE payload_json LIKE ? ORDER BY created DESC LIMIT ?",
                (needle, limit),
            ).fetchall()
        return [json.loads(row[0]) for row in rows]

    def search_entities(self, text: str, limit: int = 20) -> list[dict[str, Any]]:
        with self._connect() as db:
            if fts_available(db):
                try:
                    rows = db.execute(
                        "SELECT e.payload_json FROM creative_entity_fts f JOIN creative_entities e ON e.entity_key=f.entity_key WHERE creative_entity_fts MATCH ? ORDER BY bm25(creative_entity_fts) LIMIT ?",
                        (text, limit),
                    ).fetchall()
                    return [json.loads(row[0]) for row in rows]
                except sqlite3.OperationalError:
                    pass
            needle = f"%{text}%"
            rows = db.execute(
                "SELECT payload_json FROM creative_entities WHERE title LIKE ? OR payload_json LIKE ? ORDER BY kind,title LIMIT ?",
                (needle, needle, limit),
            ).fetchall()
        return [json.loads(row[0]) for row in rows]

    def entity_kind_counts(self) -> dict[str, int]:
        with self._connect() as db:
            rows = db.execute("SELECT kind, COUNT(*) AS n FROM creative_entities GROUP BY kind ORDER BY n DESC, kind").fetchall()
        return {row["kind"]: int(row["n"]) for row in rows}

    def model_counts(self) -> dict[str, int]:
        with self._connect() as db:
            rows = db.execute(
                "SELECT COALESCE(model_version,'<unknown>') AS model, COUNT(*) AS n FROM generations GROUP BY model ORDER BY n DESC"
            ).fetchall()
        return {row["model"]: int(row["n"]) for row in rows}

    def request_type_counts(self) -> dict[str, int]:
        with self._connect() as db:
            rows = db.execute(
                "SELECT COALESCE(request_type,'<unknown>') AS kind, COUNT(*) AS n FROM generations GROUP BY kind ORDER BY n DESC"
            ).fetchall()
        return {row["kind"]: int(row["n"]) for row in rows}

    def lineage(self, entity_key: str) -> list[dict[str, Any]]:
        with self._connect() as db:
            rows = db.execute(
                "SELECT source,target,kind,metadata_json FROM graph_edges WHERE source=? OR target=? ORDER BY kind,source,target",
                (entity_key, entity_key),
            ).fetchall()
        return [
            {"source": r["source"], "target": r["target"], "kind": r["kind"], "metadata": json.loads(r["metadata_json"])}
            for r in rows
        ]

    def provenance(self, entity_key: str) -> list[dict[str, Any]]:
        with self._connect() as db:
            rows = db.execute(
                "SELECT source,observed_at,locator,confidence,metadata_json FROM provenance WHERE entity_key=? ORDER BY observed_at",
                (entity_key,),
            ).fetchall()
        return [
            {
                "source": r["source"],
                "observed_at": r["observed_at"],
                "locator": r["locator"] or None,
                "confidence": r["confidence"],
                "metadata": json.loads(r["metadata_json"]),
            }
            for r in rows
        ]

    def assets_for_response(self, response_id: str) -> list[dict[str, Any]]:
        with self._connect() as db:
            rows = db.execute("SELECT payload_json FROM assets WHERE response_id=?", (response_id,)).fetchall()
        return [json.loads(row[0]) for row in rows]

    def stats(self) -> dict[str, int]:
        tables = (
            "generations",
            "responses",
            "assets",
            "collections",
            "profiles",
            "creative_entities",
            "graph_edges",
            "provenance",
        )
        with self._connect() as db:
            return {table: int(db.execute(f"SELECT COUNT(*) FROM {table}").fetchone()[0]) for table in tables}
