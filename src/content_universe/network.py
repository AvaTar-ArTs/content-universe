from __future__ import annotations

import json
from collections import Counter
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Any
from urllib.parse import urlsplit, urlunsplit


@dataclass(slots=True)
class EndpointStat:
    method: str
    path: str
    count: int = 0
    statuses: dict[int, int] = field(default_factory=dict)
    mime_types: dict[str, int] = field(default_factory=dict)
    sample_urls: list[str] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def canonical_url(url: str) -> str:
    parts = urlsplit(url)
    return urlunsplit((parts.scheme, parts.netloc, parts.path, "", ""))


def endpoint_inventory(path: str | Path, *, host: str | None = None) -> list[EndpointStat]:
    payload = json.loads(Path(path).read_text(encoding="utf-8"))
    grouped: dict[tuple[str, str], EndpointStat] = {}

    for entry in ((payload.get("log") or {}).get("entries") or []):
        request = entry.get("request") or {}
        response = entry.get("response") or {}
        url = str(request.get("url") or "")
        parts = urlsplit(url)
        if host and parts.hostname != host:
            continue
        method = str(request.get("method") or "GET").upper()
        key = (method, parts.path)
        stat = grouped.setdefault(key, EndpointStat(method=method, path=parts.path))
        stat.count += 1
        status = response.get("status")
        if isinstance(status, int):
            stat.statuses[status] = stat.statuses.get(status, 0) + 1
        mime = str(((response.get("content") or {}).get("mimeType") or "")).split(";", 1)[0]
        if mime:
            stat.mime_types[mime] = stat.mime_types.get(mime, 0) + 1
        safe = canonical_url(url)
        if safe not in stat.sample_urls and len(stat.sample_urls) < 3:
            stat.sample_urls.append(safe)

    return sorted(grouped.values(), key=lambda item: (-item.count, item.path, item.method))


def endpoint_summary(path: str | Path, *, host: str | None = None) -> dict[str, Any]:
    inventory = endpoint_inventory(path, host=host)
    return {
        "endpoint_count": len(inventory),
        "request_count": sum(item.count for item in inventory),
        "methods": dict(Counter(item.method for item in inventory)),
        "endpoints": [item.to_dict() for item in inventory],
    }
