import json

import pytest

from content_universe.bulk import discover_folder_sources
from content_universe.pipeline import harvest_sources


def _write_suno(path, *, title="Bulk Song"):
    path.write_text(
        json.dumps(
            {
                "songs": [
                    {
                        "id": "123e4567-e89b-12d3-a456-426614174099",
                        "title": title,
                        "audioUrl": "https://example.invalid/song.mp3",
                        "prompt": "bulk prompt",
                        "lyrics": "bulk lyrics",
                    }
                ]
            }
        ),
        encoding="utf-8",
    )


def test_discover_folder_sources_recurses_and_classifies(tmp_path):
    _write_suno(tmp_path / "suno-export.json")
    nested = tmp_path / "nested"
    nested.mkdir()
    _write_suno(nested / "another.json", title="Nested Song")
    (tmp_path / "notes.txt").write_text("not supported", encoding="utf-8")

    discovery = discover_folder_sources(tmp_path)

    assert [path.name for path in discovery.supported] == ["another.json", "suno-export.json"]
    assert [path.name for path in discovery.unsupported] == ["notes.txt"]
    assert discovery.skipped == []

    universe = harvest_sources(discovery.supported)
    assert len(universe.generations) == 2


def test_discover_folder_sources_filters_and_ignores_common_dependency_dirs(tmp_path):
    _write_suno(tmp_path / "keep.json")
    _write_suno(tmp_path / "skip.json")
    dependency = tmp_path / "node_modules"
    dependency.mkdir()
    _write_suno(dependency / "hidden.json")

    discovery = discover_folder_sources(tmp_path, include=["*.json"], exclude=["skip.json"])

    assert [path.name for path in discovery.supported] == ["keep.json"]
    assert sorted(path.name for path in discovery.skipped) == ["hidden.json", "skip.json"]


def test_discover_folder_sources_can_be_non_recursive(tmp_path):
    _write_suno(tmp_path / "top.json")
    nested = tmp_path / "nested"
    nested.mkdir()
    _write_suno(nested / "nested.json")

    discovery = discover_folder_sources(tmp_path, recursive=False)

    assert [path.name for path in discovery.supported] == ["top.json"]


def test_discover_folder_sources_validates_inputs(tmp_path):
    with pytest.raises(FileNotFoundError):
        discover_folder_sources(tmp_path / "missing")

    file_path = tmp_path / "file.json"
    file_path.write_text("{}", encoding="utf-8")
    with pytest.raises(NotADirectoryError):
        discover_folder_sources(file_path)

    with pytest.raises(ValueError):
        discover_folder_sources(tmp_path, max_files=0)
