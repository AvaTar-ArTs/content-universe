from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Callable, Iterator, Mapping
from urllib.parse import urlencode

from ...catalog import GenerationRecord
from ...ideogram import generation_from_raw

PROFILE_ENDPOINT = "https://ideogram.ai/api/g/u/profile/c"


@dataclass(slots=True)
class ProfilePage:
    url: str
    payload: dict[str, Any]
    records: list[GenerationRecord]
    next_cursor: str | None


Transport = Callable[[str], Mapping[str, Any]]


def build_profile_url(handle: str, *, cursor: str | None = None, sort_filter: str = "DEFAULT") -> str:
    params = {"display_handle": handle, "sort_filter": sort_filter}
    if cursor:
        params["cursor"] = cursor
    return f"{PROFILE_ENDPOINT}?{urlencode(params)}"


def extract_profile_records(payload: Mapping[str, Any], source: str) -> list[GenerationRecord]:
    """Extract top-level generation-shaped records from a profile page payload.

    Ideogram has changed container field names over time, so this routine checks
    common list containers first and then performs a shallow fallback search.
    """
    candidates: list[Any] = []
    for key in ("results", "generations", "items", "data"):
        value = payload.get(key)
        if isinstance(value, list):
            candidates.extend(value)
    if not candidates:
        candidates.extend(v for v in payload.values() if isinstance(v, list))

    records: list[GenerationRecord] = []
    seen: set[str] = set()
    for item in candidates:
        if not isinstance(item, dict) or not item.get("request_id"):
            continue
        record = generation_from_raw(item, source)
        if record and record.request_id not in seen:
            seen.add(record.request_id)
            records.append(record)
    return records


def walk_profile(
    handle: str,
    transport: Transport,
    *,
    sort_filter: str = "DEFAULT",
    max_pages: int | None = None,
) -> Iterator[ProfilePage]:
    """Walk Ideogram profile pages using a caller-controlled transport.

    Content Universe deliberately does not own browser cookies or session tokens.
    A CLI/browser integration can inject an authenticated transport while tests
    and offline tools can inject fixture transports.
    """
    cursor: str | None = None
    page_number = 0
    seen_cursors: set[str] = set()

    while True:
        url = build_profile_url(handle, cursor=cursor, sort_filter=sort_filter)
        raw = transport(url)
        payload = dict(raw)
        records = extract_profile_records(payload, f"ideogram-profile:{handle}:page:{page_number}")
        next_cursor = payload.get("next_cursor") or payload.get("nextCursor")
        yield ProfilePage(url=url, payload=payload, records=records, next_cursor=str(next_cursor) if next_cursor else None)

        page_number += 1
        if max_pages is not None and page_number >= max_pages:
            break
        if not next_cursor:
            break
        next_cursor = str(next_cursor)
        if next_cursor in seen_cursors:
            break
        seen_cursors.add(next_cursor)
        cursor = next_cursor
