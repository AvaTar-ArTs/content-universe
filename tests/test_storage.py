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
