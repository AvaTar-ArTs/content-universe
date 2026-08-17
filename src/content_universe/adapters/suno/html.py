from __future__ import annotations

import json
import re
from html.parser import HTMLParser
from pathlib import Path
from typing import Any, Iterable

from ...adapters.base import Adapter, HarvestResult
from ...catalog import GenerationRecord, ResponseRecord
from ...graph import GraphEdge
from ...models import EdgeKind, EntityKind, EntityRef
from ...provenance import Observation

UUID_RE = re.compile(r"[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12}")
SONG_LINK_RE = re.compile(r"https?://(?:www\.)?suno\.com/(?:song|clip)/([0-9a-fA-F-]{36})|/(?:song|clip)/([0-9a-fA-F-]{36})")


class _NextDataParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.in_next_data = False
        self.buffer: list[str] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        if tag != "script":
            return
        data = {k: v or "" for k, v in attrs}
        if data.get("id") == "__NEXT_DATA__":
            self.in_next_data = True

    def handle_endtag(self, tag: str) -> None:
        if tag == "script" and self.in_next_data:
            self.in_next_data = False

    def handle_data(self, data: str) -> None:
        if self.in_next_data:
            self.buffer.append(data)

    @property
    def next_data(self) -> Any:
        if not self.buffer:
            return None
        try:
            return json.loads("".join(self.buffer))
        except json.JSONDecodeError:
            return None


def _walk(value: Any) -> Iterable[dict[str, Any]]:
    if isinstance(value, dict):
        yield value
        for child in value.values():
            yield from _walk(child)
    elif isinstance(value, list):
        for child in value:
            yield from _walk(child)


def _extract_id(item: dict[str, Any]) -> str | None:
    for key in ("id", "clip_id", "song_id", "uuid"):
        value = item.get(key)
        if isinstance(value, str):
            match = UUID_RE.search(value)
            if match:
                return match.group(0)
    for key in ("url", "audio_url", "audioUrl", "image_url", "imageUrl"):
        value = item.get(key)
        if isinstance(value, str):
            match = UUID_RE.search(value)
            if match:
                return match.group(0)
    return None


def _looks_like_song(item: dict[str, Any]) -> bool:
    keys = {str(k).lower() for k in item}
    signals = {"audio_url", "audiourl", "lyrics", "title", "metadata", "image_url", "imageurl", "prompt", "tags"}
    return bool(keys & signals) and _extract_id(item) is not None


def _record_from_song(item: dict[str, Any], source: str) -> GenerationRecord | None:
    song_id = _extract_id(item)
    if not song_id:
        return None
    metadata = item.get("metadata") if isinstance(item.get("metadata"), dict) else {}
    prompt = item.get("prompt") or metadata.get("prompt")
    title = item.get("title") or metadata.get("title")
    lyrics = item.get("lyrics") or metadata.get("lyrics")
    tags = item.get("tags") or metadata.get("tags")
    image_url = item.get("image_url") or item.get("imageUrl") or metadata.get("image_url")
    audio_url = item.get("audio_url") or item.get("audioUrl") or metadata.get("audio_url")

    request_id = f"suno:{song_id}"
    record = GenerationRecord(
        request_id=request_id,
        request_type="AUDIO_GENERATION",
        user_prompt=str(prompt) if prompt is not None else None,
        caption=str(item.get("description") or metadata.get("description") or "") or None,
        raw=dict(item),
        sources=[source],
    )
    response = ResponseRecord(
        response_id=song_id,
        prompt=prompt,
        asset_url=str(audio_url) if audio_url else None,
        raw={
            "title": title,
            "lyrics": lyrics,
            "tags": tags,
            "image_url": image_url,
            "metadata": metadata,
            "source_object": item,
        },
        sources=[source],
    )
    record.responses[song_id] = response
    return record


class SunoHtmlAdapter(Adapter):
    name = "suno-html"

    def supports(self, source: str | Path) -> bool:
        path = Path(source)
        if path.suffix.lower() not in {".html", ".htm"}:
            return False
        try:
            head = path.read_text(encoding="utf-8", errors="ignore")[:30000].lower()
        except OSError:
            return False
        return "suno" in head or "__next_data__" in head

    def harvest(self, source: str | Path) -> HarvestResult:
        path = Path(source)
        text = path.read_text(encoding="utf-8", errors="ignore")
        result = HarvestResult(metadata={"source": str(path)})
        parser = _NextDataParser()
        parser.feed(text)
        found_ids: set[str] = set()

        next_data = parser.next_data
        if next_data is not None:
            for item in _walk(next_data):
                if not _looks_like_song(item):
                    continue
                record = _record_from_song(item, f"{self.name}:next-data")
                if record:
                    result.records.append(record)
                    found_ids.add(next(iter(record.responses)))

        # Fallback: recover stable song identities even when metadata shape changes.
        for match in SONG_LINK_RE.finditer(text):
            song_id = match.group(1) or match.group(2)
            if not song_id or song_id in found_ids:
                continue
            request_id = f"suno:{song_id}"
            record = GenerationRecord(request_id=request_id, request_type="AUDIO_GENERATION", sources=[f"{self.name}:link-fallback"])
            record.responses[song_id] = ResponseRecord(response_id=song_id, sources=[f"{self.name}:link-fallback"])
            result.records.append(record)
            found_ids.add(song_id)

        for song_id in found_ids:
            req = EntityRef(EntityKind.GENERATION, f"suno:{song_id}")
            res = EntityRef(EntityKind.RESPONSE, song_id)
            result.graph.add(GraphEdge(req, res, EdgeKind.PRODUCED))
            result.provenance.add(res.key, Observation(source=self.name, locator=str(path)))

        result.metadata["song_ids"] = len(found_ids)
        result.metadata["next_data_found"] = next_data is not None
        return result
