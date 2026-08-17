from __future__ import annotations

import csv
import re
from pathlib import Path
from typing import Any

from ...adapters.base import Adapter, HarvestResult
from ...catalog import GenerationRecord, ResponseRecord
from ...graph import GraphEdge
from ...models import EdgeKind, EntityKind, EntityRef
from ...provenance import Observation

UUID_RE = re.compile(r"[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12}")


def _first(row: dict[str, Any], *keys: str) -> str | None:
    lowered = {str(k).lower().replace("_", "").replace(" ", ""): v for k, v in row.items()}
    for key in keys:
        value = lowered.get(key.lower().replace("_", "").replace(" ", ""))
        if value not in (None, ""):
            return str(value)
    return None


def _song_id(row: dict[str, Any]) -> str | None:
    direct = _first(row, "id", "song_id", "clip_id", "uuid")
    if direct:
        match = UUID_RE.search(direct)
        return match.group(0) if match else direct
    for key in ("url", "suno link", "shareurl", "audiourl", "audio url"):
        value = _first(row, key)
        if value:
            match = UUID_RE.search(value)
            if match:
                return match.group(0)
    return None


class SunoCsvAdapter(Adapter):
    name = "suno-csv"

    def supports(self, source: str | Path) -> bool:
        path = Path(source)
        if path.suffix.lower() != ".csv":
            return False
        try:
            head = path.read_text(encoding="utf-8", errors="ignore")[:20000].lower()
        except OSError:
            return False
        markers = ("suno", "audiourl", "audio url", "lyrics", "suno link")
        return any(marker in head for marker in markers)

    def harvest(self, source: str | Path) -> HarvestResult:
        path = Path(source)
        result = HarvestResult(metadata={"source": str(path)})
        by_id: dict[str, GenerationRecord] = {}

        with path.open("r", encoding="utf-8-sig", errors="replace", newline="") as handle:
            reader = csv.DictReader(handle)
            for row_number, row in enumerate(reader, start=2):
                song_id = _song_id(row)
                if not song_id:
                    result.warnings.append(f"row {row_number}: no stable song ID")
                    continue
                request_id = f"suno:{song_id}"
                record = GenerationRecord(
                    request_id=request_id,
                    request_type="AUDIO_GENERATION",
                    user_prompt=_first(row, "prompt", "image prompt", "generation prompt"),
                    caption=_first(row, "description", "summary"),
                    raw={"csv_row": dict(row)},
                    sources=[self.name],
                )
                response = ResponseRecord(
                    response_id=str(song_id),
                    prompt=_first(row, "prompt", "generation prompt"),
                    asset_url=_first(row, "audioUrl", "audio url", "mp3", "audio"),
                    raw={
                        "title": _first(row, "title", "song title"),
                        "lyrics": _first(row, "lyrics"),
                        "tags": _first(row, "tags", "genres", "style"),
                        "image_url": _first(row, "imageUrl", "image url", "cover url", "cover"),
                        "duration": _first(row, "duration"),
                        "suno_url": _first(row, "url", "suno link", "shareUrl"),
                        "csv_row": dict(row),
                    },
                    sources=[self.name],
                )
                record.responses[response.response_id] = response

                existing = by_id.get(request_id)
                if existing is None:
                    by_id[request_id] = record
                else:
                    # Let the shared Catalog perform richer-record merge later.
                    result.records.append(record)

                req = EntityRef(EntityKind.GENERATION, request_id)
                res = EntityRef(EntityKind.RESPONSE, str(song_id))
                result.graph.add(GraphEdge(req, res, EdgeKind.PRODUCED))
                result.provenance.add(res.key, Observation(source=self.name, locator=f"{path}:row:{row_number}"))

        result.records.extend(by_id.values())
        result.metadata["rows_with_ids"] = len(by_id)
        return result
