from __future__ import annotations

import hashlib
import json
import re
import urllib.request
from dataclasses import dataclass, field, asdict
from pathlib import Path
from typing import Iterable
from urllib.parse import urlparse

from ...catalog import GenerationRecord
from ...ideogram import extract_response_id_from_asset_url

ASSET_RE = re.compile(r"/assets/image/([^/]+)/response/([^/@?]+)(?:@([^/?]+))?")
ALLOWED_HOSTS = {"ideogram.ai", "www.ideogram.ai"}


@dataclass(slots=True)
class AssetManifestEntry:
    response_id: str
    request_id: str | None = None
    url: str | None = None
    representation: str | None = None
    resolution: str | None = None
    filename: str | None = None
    sha256: str | None = None
    downloaded: bool = False
    metadata: dict = field(default_factory=dict)

    def to_dict(self) -> dict:
        return asdict(self)


def parse_asset_url(url: str) -> dict[str, str | None]:
    match = ASSET_RE.search(url)
    if not match:
        return {"representation": None, "response_id": extract_response_id_from_asset_url(url), "resolution": None}
    return {"representation": match.group(1), "response_id": match.group(2), "resolution": match.group(3)}


def manifest_from_records(records: Iterable[GenerationRecord]) -> list[AssetManifestEntry]:
    entries: list[AssetManifestEntry] = []
    seen: set[tuple[str, str]] = set()
    for generation in records:
        for response in generation.responses.values():
            if not response.asset_url:
                continue
            parsed = parse_asset_url(response.asset_url)
            response_id = parsed["response_id"] or response.response_id
            key = (response_id, response.asset_url)
            if key in seen:
                continue
            seen.add(key)
            entries.append(AssetManifestEntry(
                response_id=response_id,
                request_id=generation.request_id,
                url=response.asset_url,
                representation=parsed["representation"],
                resolution=parsed["resolution"],
            ))
    return entries


def write_manifest(entries: Iterable[AssetManifestEntry], path: str | Path) -> Path:
    out = Path(path)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps([e.to_dict() for e in entries], indent=2, ensure_ascii=False), encoding="utf-8")
    return out


def download_public_assets(entries: Iterable[AssetManifestEntry], directory: str | Path, *, timeout: int = 30) -> list[AssetManifestEntry]:
    """Download already-public asset URLs from an explicit allowlist.

    This function does not copy cookies, authorization headers, or browser session
    state. Private/authenticated downloads belong in caller-controlled tooling.
    """
    root = Path(directory)
    root.mkdir(parents=True, exist_ok=True)
    result: list[AssetManifestEntry] = []

    for entry in entries:
        if not entry.url:
            result.append(entry)
            continue
        parsed = urlparse(entry.url)
        if parsed.scheme != "https" or parsed.hostname not in ALLOWED_HOSTS:
            entry.metadata["download_error"] = "URL host not allowlisted"
            result.append(entry)
            continue
        suffix = Path(parsed.path).suffix or ".bin"
        filename = entry.filename or f"{entry.response_id}{suffix}"
        target = root / filename
        try:
            req = urllib.request.Request(entry.url, headers={"User-Agent": "Content-Universe/0.2"})
            with urllib.request.urlopen(req, timeout=timeout) as response:
                data = response.read()
            target.write_bytes(data)
            entry.filename = filename
            entry.sha256 = hashlib.sha256(data).hexdigest()
            entry.downloaded = True
        except Exception as exc:  # field utility: retain failure in manifest
            entry.metadata["download_error"] = f"{type(exc).__name__}: {exc}"
        result.append(entry)
    return result
