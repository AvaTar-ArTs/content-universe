import json
import sqlite3

from content_universe.catalog import GenerationRecord, ResponseRecord
from content_universe.graph import CreativeGraph, GraphEdge
from content_universe.models import EdgeKind, EntityKind, EntityRef
from content_universe.provenance import Observation, ProvenanceLedger
from content_universe.query import CatalogQuery
from content_universe.storage import SQLiteStore


def test_sqlite_round_trip(tmp_path):
    path = tmp_path / "catalog.sqlite"
    record = GenerationRecord(request_id="req", model_version="V_4_0", user_prompt="moon poster")
    record.responses["resp"] = ResponseRecord(response_id="resp", response_index=0)
    graph = CreativeGraph()
    graph.add(GraphEdge(EntityRef(EntityKind.GENERATION, "req"), EntityRef(EntityKind.RESPONSE, "resp"), EdgeKind.PRODUCED))
    ledger = ProvenanceLedger()
    ledger.add("generation:req", Observation(source="fixture", locator="test"))

    with SQLiteStore(path) as store:
        store.upsert_many([record])
        store.save_graph(graph)
        store.save_provenance(ledger)
        assert store.stats()["generations"] == 1
        assert store.stats()["responses"] == 1

    query = CatalogQuery(path)
    assert query.generation("req")["user_prompt"] == "moon poster"
    assert query.response("resp")["response_id"] == "resp"
    assert len(query.search_prompts("moon")) == 1
    assert query.model_counts() == {"V_4_0": 1}
    assert query.lineage("generation:req")[0]["kind"] == "produced"


def test_graph_storage_preserves_distinct_instance_edges(tmp_path):
    path = tmp_path / "instances.sqlite"
    graph = CreativeGraph()
    scene = EntityRef(EntityKind.SCENE_GRAPH, "scene-1")
    hero = EntityRef(EntityKind.CHARACTER, "hero")
    graph.add(GraphEdge(scene, hero, EdgeKind.INSTANCE_OF, {"element_id": "hero-left"}, edge_id="hero-left"))
    graph.add(GraphEdge(scene, hero, EdgeKind.INSTANCE_OF, {"element_id": "hero-right"}, edge_id="hero-right"))

    with SQLiteStore(path) as store:
        store.save_graph(graph)
        rows = store.db.execute(
            "SELECT edge_id, metadata_json FROM graph_edges WHERE source=? AND target=? AND kind=? ORDER BY edge_id",
            (scene.key, hero.key, EdgeKind.INSTANCE_OF.value),
        ).fetchall()

    assert [row[0] for row in rows] == ["hero-left", "hero-right"]
    assert [json.loads(row[1])["element_id"] for row in rows] == ["hero-left", "hero-right"]


def test_existing_catalog_graph_schema_migrates_without_losing_edges(tmp_path):
    path = tmp_path / "legacy.sqlite"
    db = sqlite3.connect(path)
    db.execute(
        """
        CREATE TABLE graph_edges (
          source TEXT NOT NULL,
          target TEXT NOT NULL,
          kind TEXT NOT NULL,
          metadata_json TEXT NOT NULL,
          PRIMARY KEY(source, target, kind)
        )
        """
    )
    db.execute(
        "INSERT INTO graph_edges(source,target,kind,metadata_json) VALUES(?,?,?,?)",
        ("generation:req", "response:resp", "produced", '{"legacy":true}'),
    )
    db.commit()
    db.close()

    with SQLiteStore(path) as store:
        columns = {row[1] for row in store.db.execute("PRAGMA table_info(graph_edges)").fetchall()}
        row = store.db.execute(
            "SELECT source,target,kind,edge_id,metadata_json FROM graph_edges"
        ).fetchone()

    assert "edge_id" in columns
    assert row[:4] == ("generation:req", "response:resp", "produced", "")
    assert json.loads(row[4]) == {"legacy": True}
