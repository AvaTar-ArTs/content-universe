from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from ...adapters.base import Adapter, HarvestResult
from ...catalog import GenerationRecord, ResponseRecord
from ...graph import GraphEdge
from ...models import EdgeKind, EntityKind, EntityRef
from ...provenance import Observation


class IdeogramBrowserExportAdapter(Adapter):
    name = "ideogram-browser-export"

    def _items(self, path: Path) -> list[dict[str, Any]]:
        try:
            payload = json.loads(path.read_text(encoding="utf-8"))
        except (json.JSONDecodeError, OSError):
            return []
        if isinstance(payload, list):
            return [item for item in payload if isinstance(item, dict)]
        if isinstance(payload, dict) and isinstance(payload.get("items"), list):
            return [item for item in payload["items"] if isinstance(item, dict)]
        return []

    def supports(self, source: str | Path) -> bool:
        path = Path(source)
        if path.suffix.lower() != ".json":
            return False
        items = self._items(path)
        return bool(items) and any(
            item.get("platform") == "ideogram" and item.get("generation_id")
            for item in items[:20]
        )

    def harvest(self, source: str | Path) -> HarvestResult:
        path = Path(source)
        items = self._items(path)
        result = HarvestResult(metadata={"source": str(path), "browser_observations": len(items)})
        records: dict[str, GenerationRecord] = {}

        for item in items:
            generation_id = item.get("generation_id")
            if not generation_id:
                continue
            generation_id = str(generation_id)
            record = records.setdefault(generation_id, GenerationRecord(request_id=generation_id, sources=[self.name]))
            response_id = item.get("response_id")
            if response_id:
                response_id = str(response_id)
                response = record.responses.setdefault(response_id, ResponseRecord(response_id=response_id, sources=[self.name]))
                index = item.get("response_index")
                response.response_index = int(index) if isinstance(index, int) or (isinstance(index, str) and index.isdigit()) else response.response_index
                response.asset_url = item.get("asset_url") or response.asset_url
                response.raw = {**response.raw, "browser_observation": item}

                req_ref = EntityRef(EntityKind.GENERATION, generation_id)
                res_ref = EntityRef(EntityKind.RESPONSE, response_id)
                result.graph.add(GraphEdge(req_ref, res_ref, EdgeKind.PRODUCED, {"response_index": response.response_index}))
                result.provenance.add(
                    res_ref.key,
                    Observation(
                        source=self.name,
                        observed_at=str(item.get("observed_at")) if item.get("observed_at") else Observation(source=self.name).observed_at,
                        locator=item.get("generation_url") or item.get("asset_url"),
                        metadata={"feed": item.get("feed")},
                    ),
                )
        result.records = list(records.values())
        return result
