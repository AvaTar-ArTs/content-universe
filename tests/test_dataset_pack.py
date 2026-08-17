import json
import zipfile

from content_universe.catalog import GenerationRecord, ResponseRecord
from content_universe.dataset_pack import build_dataset_pack
from content_universe.universe import ContentUniverse


def test_dataset_pack_contains_normalized_bundle(tmp_path):
    universe = ContentUniverse()
    generation = GenerationRecord(request_id="req-pack", user_prompt="pack prompt", sources=["fixture"])
    generation.responses["resp-pack"] = ResponseRecord(response_id="resp-pack", sources=["fixture"])
    universe.ingest_generation(generation)

    output = tmp_path / "pack.zip"
    build_dataset_pack(universe, output)
    assert output.exists()

    with zipfile.ZipFile(output) as archive:
        names = set(archive.namelist())
        assert {"pack.json", "universe.json", "generations.jsonl", "graph.json", "graph.mmd", "provenance.json", "asset-manifest.json", "audit.json"} <= names
        manifest = json.loads(archive.read("pack.json"))
        assert manifest["format"] == "content-universe-dataset-pack"
        assert manifest["summary"]["generation_count"] == 1
