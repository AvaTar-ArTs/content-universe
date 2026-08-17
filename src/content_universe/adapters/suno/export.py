from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from ...adapters.base import Adapter, HarvestResult
from ...catalog import GenerationRecord, ResponseRecord
from ...graph import GraphEdge
from ...models import EdgeKind, EntityKind, EntityRef
from ...provenance import Observation


class SunoExportAdapter(Adapter):
    """Normalize existing Suno JSON exports into the shared creative catalog.

    This intentionally starts with exported/recovered JSON rather than live scraping.
    Browser extraction remains a separate field collector, mirroring the historical
    Suno extractor architecture without coupling the core to Suno's DOM.
    """

    name = "suno-export"

    def supports(self, source: str | Path) -> bool:
        p = Path(source)
        if p.suffix.lower() != ".json":
            return False
        head = p.read_text(encoding="utf-8", errors="ignore")[:10000].lower()
        return "suno" in head or "audiourl" in head or "lyrics" in head

    def harvest(self, source: str | Path) -> HarvestResult:
        path = Path(source)
        payload: Any = json.loads(path.read_text(encoding="utf-8"))
        items = payload if isinstance(payload, list) else payload.get("songs", payload.get("items", []))
        result = HarvestResult(metadata={"source": str(path)})

        for raw in items if isinstance(items, list) else []:
            if not isinstance(raw, dict):
                continue
            song_id = raw.get("id") or raw.get("song_id")
            if not song_id:
                continue
            request_id = f"suno:{song_id}"
            record = GenerationRecord(
                request_id=request_id,
                request_type="AUDIO_GENERATION",
                user_prompt=raw.get("prompt"),
                caption=raw.get("description") or raw.get("summary"),
                creation_time_float=raw.get("created_at") if isinstance(raw.get("created_at"), (int, float)) else None,
                raw=dict(raw),
                sources=[self.name],
            )
            response = ResponseRecord(
                response_id=str(song_id),
                prompt=raw.get("prompt"),
                asset_url=raw.get("audioUrl") or raw.get("audio_url"),
                likes=raw.get("likes") if isinstance(raw.get("likes"), int) else None,
                raw={"title": raw.get("title"), "lyrics": raw.get("lyrics"), "tags": raw.get("tags"), "image_url": raw.get("imageUrl") or raw.get("image_url"), **raw},
                sources=[self.name],
            )
            record.responses[response.response_id] = response
            result.records.append(record)
            req = EntityRef(EntityKind.GENERATION, request_id)
            res = EntityRef(EntityKind.RESPONSE, response.response_id)
            result.graph.add(GraphEdge(req, res, EdgeKind.PRODUCED))
            result.provenance.add(res.key, Observation(source=self.name, locator=str(path)))
        return result
