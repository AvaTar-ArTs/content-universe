from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any, Iterable

from .catalog import Catalog, GenerationRecord, ResponseRecord

PROFILE_PATH_FRAGMENT = "/api/g/u/profile/c"
ASSET_RE = re.compile(r"/response/([^/@?]+)(?:@[^/?]+)?")


def _walk_json(value: Any) -> Iterable[Any]:
    yield value
    if isinstance(value, dict):
        for child in value.values():
            yield from _walk_json(child)
    elif isinstance(value, list):
        for child in value:
            yield from _walk_json(child)


def _generation_candidates(payload: Any) -> Iterable[dict[str, Any]]:
    """Yield dicts that look like Ideogram generation request records."""
    seen: set[int] = set()
    for value in _walk_json(payload):
        if not isinstance(value, dict):
            continue
        if "request_id" not in value or "responses" not in value:
            continue
        marker = id(value)
        if marker in seen:
            continue
        seen.add(marker)
        yield value


def response_from_raw(raw: dict[str, Any], source: str) -> ResponseRecord | None:
    response_id = raw.get("response_id")
    if not response_id:
        return None
    asset_url = raw.get("image_url") or raw.get("url")
    return ResponseRecord(
        response_id=str(response_id),
        response_index=raw.get("response_index"),
        prompt=raw.get("prompt"),
        asset_url=asset_url,
        format=raw.get("format"),
        likes=raw.get("num_likes"),
        private=raw.get("private"),
        raw=dict(raw),
        sources=[source],
    )


def generation_from_raw(raw: dict[str, Any], source: str) -> GenerationRecord | None:
    request_id = raw.get("request_id")
    if not request_id:
        return None

    record = GenerationRecord(
        request_id=str(request_id),
        request_type=raw.get("request_type"),
        user_prompt=raw.get("user_prompt"),
        user_negative_prompt=raw.get("user_negative_prompt"),
        caption=raw.get("caption"),
        seed=raw.get("seed"),
        model_version=raw.get("model_version"),
        model_uri=raw.get("model_uri"),
        width=raw.get("width"),
        height=raw.get("height"),
        aspect_ratio=raw.get("aspect_ratio") or (raw.get("user_hparams") or {}).get("aspect_ratio"),
        image_resolution=raw.get("image_resolution"),
        style_expert=raw.get("style_expert"),
        creation_time_float=raw.get("creation_time_float"),
        private=raw.get("private"),
        completed=raw.get("is_completed"),
        errored=raw.get("is_errored"),
        references=raw.get("references") or {},
        character_reference_collection_ids=raw.get("character_reference_collection_ids") or [],
        product_reference_collection_ids=raw.get("product_reference_collection_ids") or [],
        style_reference_collection_ids=raw.get("style_reference_collection_ids") or [],
        raw=dict(raw),
        sources=[source],
    )

    for item in raw.get("responses") or []:
        if not isinstance(item, dict):
            continue
        response = response_from_raw(item, source)
        if response:
            record.responses[response.response_id] = response
    return record


def _decode_har_content(content: dict[str, Any]) -> str | None:
    text = content.get("text")
    if not isinstance(text, str):
        return None
    if content.get("encoding") == "base64":
        import base64

        try:
            return base64.b64decode(text).decode("utf-8", errors="replace")
        except Exception:
            return None
    return text


def catalog_from_har(path: str | Path) -> Catalog:
    """Parse Ideogram generation/profile records from a saved HAR, offline."""
    har_path = Path(path)
    payload = json.loads(har_path.read_text(encoding="utf-8"))
    entries = ((payload.get("log") or {}).get("entries") or [])
    catalog = Catalog()

    for index, entry in enumerate(entries):
        request = entry.get("request") or {}
        response = entry.get("response") or {}
        url = request.get("url") or ""
        content = response.get("content") or {}
        text = _decode_har_content(content)
        if not text:
            continue

        mime = (content.get("mimeType") or "").lower()
        if "json" not in mime and not text.lstrip().startswith(("{", "[")):
            continue

        try:
            body = json.loads(text)
        except json.JSONDecodeError:
            continue

        source = f"har:{har_path.name}:{index}:{url}"
        for candidate in _generation_candidates(body):
            record = generation_from_raw(candidate, source)
            if record:
                catalog.ingest(record)

    return catalog


def profile_pages_from_har(path: str | Path) -> list[dict[str, Any]]:
    """Return decoded responses specifically associated with the profile cursor feed."""
    payload = json.loads(Path(path).read_text(encoding="utf-8"))
    pages: list[dict[str, Any]] = []
    for entry in ((payload.get("log") or {}).get("entries") or []):
        request = entry.get("request") or {}
        if PROFILE_PATH_FRAGMENT not in (request.get("url") or ""):
            continue
        content = ((entry.get("response") or {}).get("content") or {})
        text = _decode_har_content(content)
        if not text:
            continue
        try:
            decoded = json.loads(text)
        except json.JSONDecodeError:
            continue
        if isinstance(decoded, dict):
            pages.append(decoded)
    return pages


def extract_response_id_from_asset_url(url: str) -> str | None:
    match = ASSET_RE.search(url)
    return match.group(1) if match else None
