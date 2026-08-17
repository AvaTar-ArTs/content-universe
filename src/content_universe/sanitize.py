from __future__ import annotations

import copy
from typing import Any

SENSITIVE_HEADERS = {
    "authorization",
    "cookie",
    "set-cookie",
    "x-api-key",
    "cf-response-token",
}
SENSITIVE_QUERY_KEYS = {
    "token",
    "access_token",
    "auth",
    "authorization",
    "session",
    "session_id",
    "code",
}


def _redact_headers(headers: list[dict[str, Any]]) -> list[dict[str, Any]]:
    cleaned: list[dict[str, Any]] = []
    for item in headers:
        name = str(item.get("name", ""))
        value = item.get("value")
        if name.lower() in SENSITIVE_HEADERS:
            value = "<REDACTED>"
        cleaned.append({**item, "value": value})
    return cleaned


def sanitize_har(payload: dict[str, Any], *, strip_response_bodies: bool = False) -> dict[str, Any]:
    """Return a public-fixture-safe HAR copy.

    This is intentionally conservative. It redacts common credential-bearing
    headers and sensitive query-string values. Callers should still review the
    result before publication because platform-specific secrets may use other
    names.
    """
    result = copy.deepcopy(payload)
    for entry in ((result.get("log") or {}).get("entries") or []):
        request = entry.get("request") or {}
        response = entry.get("response") or {}
        request["headers"] = _redact_headers(request.get("headers") or [])
        response["headers"] = _redact_headers(response.get("headers") or [])
        for item in request.get("queryString") or []:
            if str(item.get("name", "")).lower() in SENSITIVE_QUERY_KEYS:
                item["value"] = "<REDACTED>"
        post = request.get("postData") or {}
        for item in post.get("params") or []:
            if str(item.get("name", "")).lower() in SENSITIVE_QUERY_KEYS:
                item["value"] = "<REDACTED>"
        if strip_response_bodies:
            content = response.get("content") or {}
            content.pop("text", None)
            content.pop("encoding", None)
    return result
