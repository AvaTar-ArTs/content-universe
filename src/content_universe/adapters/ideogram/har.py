from __future__ import annotations

from pathlib import Path

from ...adapters.base import Adapter, HarvestResult
from ...graph import GraphEdge
from ...ideogram import catalog_from_har, profile_pages_from_har
from ...models import EdgeKind, EntityKind, EntityRef
from ...provenance import Observation


class IdeogramHarAdapter(Adapter):
    name = "ideogram-har"

    def supports(self, source: str | Path) -> bool:
        p = Path(source)
        return p.suffix.lower() == ".har" and "ideogram" in p.name.lower()

    def harvest(self, source: str | Path) -> HarvestResult:
        path = Path(source)
        catalog = catalog_from_har(path)
        result = HarvestResult(records=list(catalog.generations.values()))
        result.metadata["profile_pages"] = len(profile_pages_from_har(path))
        result.metadata["source"] = str(path)

        for record in result.records:
            req = EntityRef(EntityKind.GENERATION, record.request_id)
            result.provenance.add(req.key, Observation(source=self.name, locator=str(path)))
            for response in record.responses.values():
                res = EntityRef(EntityKind.RESPONSE, response.response_id)
                result.graph.add(GraphEdge(req, res, EdgeKind.PRODUCED, {"response_index": response.response_index}))
                result.provenance.add(res.key, Observation(source=self.name, locator=str(path)))
        return result
