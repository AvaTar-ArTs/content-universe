from __future__ import annotations

import json
import sqlite3
from pathlib import Path

FTS_SCHEMA = """
CREATE VIRTUAL TABLE IF NOT EXISTS generation_fts USING fts5(
    request_id UNINDEXED,
    content,
    tokenize='unicode61'
);
CREATE VIRTUAL TABLE IF NOT EXISTS creative_entity_fts USING fts5(
    entity_key UNINDEXED,
    content,
    tokenize='unicode61'
);
"""


def ensure_fts(db: sqlite3.Connection) -> bool:
    try:
        db.executescript(FTS_SCHEMA)
    except sqlite3.OperationalError:
        return False
    return True


def rebuild_fts(path: str | Path) -> dict[str, int | bool]:
    db = sqlite3.connect(path)
    try:
        if not ensure_fts(db):
            return {"fts5": False, "generations": 0, "creative_entities": 0}
        with db:
            db.execute("DELETE FROM generation_fts")
            db.execute("DELETE FROM creative_entity_fts")
            generation_rows = db.execute("SELECT request_id,payload_json FROM generations").fetchall()
            for request_id, payload_json in generation_rows:
                try:
                    payload = json.loads(payload_json)
                    content = json.dumps(payload, ensure_ascii=False)
                except json.JSONDecodeError:
                    content = payload_json
                db.execute("INSERT INTO generation_fts(request_id,content) VALUES(?,?)", (request_id, content))

            entity_rows = db.execute("SELECT entity_key,payload_json FROM creative_entities").fetchall()
            for entity_key, payload_json in entity_rows:
                try:
                    payload = json.loads(payload_json)
                    content = json.dumps(payload, ensure_ascii=False)
                except json.JSONDecodeError:
                    content = payload_json
                db.execute("INSERT INTO creative_entity_fts(entity_key,content) VALUES(?,?)", (entity_key, content))
        return {"fts5": True, "generations": len(generation_rows), "creative_entities": len(entity_rows)}
    finally:
        db.close()


def fts_available(db: sqlite3.Connection) -> bool:
    row = db.execute("SELECT 1 FROM sqlite_master WHERE type='table' AND name='generation_fts'").fetchone()
    return bool(row)
