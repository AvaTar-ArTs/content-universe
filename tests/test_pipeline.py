import json

from content_universe.audit import audit_records
from content_universe.manifest import universe_from_manifest
from content_universe.pipeline import harvest_sources, merge_universes


def test_pipeline_merges_suno_json_and_manifest(tmp_path):
    suno = tmp_path / "suno-export.json"
    suno.write_text(json.dumps({
        "songs": [{
            "id": "123e4567-e89b-12d3-a456-426614174099",
            "title": "Pipeline Song",
            "audioUrl": "https://example.invalid/song.mp3",
            "prompt": "pipeline prompt",
            "lyrics": "pipeline lyrics"
        }]
    }))
    manifest = tmp_path / "universe.toml"
    manifest.write_text('''
[universe]
name = "Pipeline Fixture"

[[entities]]
id = "series-pipeline"
kind = "series"
title = "Pipeline Series"
''')

    universe = harvest_sources([suno])
    merge_universes(universe, universe_from_manifest(manifest))

    assert len(universe.generations) == 1
    assert len(universe.assets) == 1
    assert len(universe.entities) == 1
    assert universe.summary()["creative_entity_kinds"] == {"series": 1}

    report = audit_records(universe.generations.values())
    assert report.generation_count == 1
    assert report.response_count == 1
