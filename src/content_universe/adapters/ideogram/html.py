from __future__ import annotations

import re
from html.parser import HTMLParser
from pathlib import Path

from ...adapters.base import Adapter, HarvestResult
from ...catalog import GenerationRecord, ResponseRecord
from ...graph import GraphEdge
from ...models import EdgeKind, EntityKind, EntityRef
from ...provenance import Observation

GRID_RE = re.compile(r"image-grid-item-([A-Za-z0-9_-]+)")
GEN_RE = re.compile(r"/g/([A-Za-z0-9_-]+)/(\d+)")
ASSET_RE = re.compile(r"/response/([A-Za-z0-9_-]+)(?:@([^/?\"']+))?")


class _Scanner(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.rows: list[dict[str, str]] = []
        self.current_generation: str | None = None

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        data = {k: v or "" for k, v in attrs}
        testid = data.get("data-testid", "")
        match = GRID_RE.search(testid)
        if match:
            self.current_generation = match.group(1)
        href = data.get("href", "")
        src = data.get("src", "")
        gm = GEN_RE.search(href)
        am = ASSET_RE.search(src)
        if gm or am:
            self.rows.append({
                "generation_id": gm.group(1) if gm else (self.current_generation or ""),
                "response_index": gm.group(2) if gm else "",
                "response_id": am.group(1) if am else "",
                "resolution": am.group(2) if am else "",
                "href": href,
                "asset_url": src,
            })


class IdeogramHtmlAdapter(Adapter):
    name = "ideogram-html"

    def supports(self, source: str | Path) -> bool:
        p = Path(source)
        return p.suffix.lower() in {".html", ".htm"} and "ideogram" in p.read_text(encoding="utf-8", errors="ignore")[:20000].lower()

    def harvest(self, source: str | Path) -> HarvestResult:
        path = Path(source)
        scanner = _Scanner()
        scanner.feed(path.read_text(encoding="utf-8", errors="ignore"))
        by_generation: dict[str, GenerationRecord] = {}
        result = HarvestResult(metadata={"source": str(path), "discovered_rows": len(scanner.rows)})

        for row in scanner.rows:
            gid = row["generation_id"]
            rid = row["response_id"]
            if not gid:
                continue
            record = by_generation.setdefault(gid, GenerationRecord(request_id=gid, sources=[self.name]))
            if rid:
                response = record.responses.setdefault(rid, ResponseRecord(response_id=rid, sources=[self.name]))
                response.asset_url = row["asset_url"] or response.asset_url
                response.response_index = int(row["response_index"]) if row["response_index"].isdigit() else response.response_index
                req_ref = EntityRef(EntityKind.GENERATION, gid)
                res_ref = EntityRef(EntityKind.RESPONSE, rid)
                result.graph.add(GraphEdge(req_ref, res_ref, EdgeKind.PRODUCED, {"response_index": response.response_index}))
                result.provenance.add(res_ref.key, Observation(source=self.name, locator=row["href"] or row["asset_url"]))
        result.records = list(by_generation.values())
        return result
