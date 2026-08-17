from __future__ import annotations

from dataclasses import asdict, dataclass, field
from typing import Any, Iterable


def _is_missing(value: Any) -> bool:
    return value is None or value == "" or value == [] or value == {}


def _deep_merge(old: Any, new: Any) -> Any:
    """Prefer useful new data without discarding useful existing data."""
    if _is_missing(old):
        return new
    if _is_missing(new):
        return old
    if isinstance(old, dict) and isinstance(new, dict):
        merged = dict(old)
        for key, value in new.items():
            merged[key] = _deep_merge(merged.get(key), value)
        return merged
    if isinstance(old, list) and isinstance(new, list):
        result = list(old)
        for item in new:
            if item not in result:
                result.append(item)
        return result
    return new


def completeness_score(data: dict[str, Any]) -> int:
    """Simple metadata completeness score used during intelligent merge."""
    score = 0
    for value in data.values():
        if _is_missing(value):
            continue
        if isinstance(value, dict):
            score += 1 + completeness_score(value)
        elif isinstance(value, list):
            score += 1 + sum(1 for item in value if not _is_missing(item))
        else:
            score += 1
    return score


@dataclass(slots=True)
class ResponseRecord:
    response_id: str
    response_index: int | None = None
    prompt: Any = None
    asset_url: str | None = None
    format: str | None = None
    likes: int | None = None
    private: bool | None = None
    raw: dict[str, Any] = field(default_factory=dict)
    sources: list[str] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(slots=True)
class GenerationRecord:
    request_id: str
    request_type: str | None = None
    user_prompt: str | None = None
    user_negative_prompt: str | None = None
    caption: str | None = None
    seed: int | None = None
    model_version: str | None = None
    model_uri: str | None = None
    width: int | None = None
    height: int | None = None
    aspect_ratio: str | None = None
    image_resolution: str | None = None
    style_expert: str | None = None
    creation_time_float: float | None = None
    private: bool | None = None
    completed: bool | None = None
    errored: bool | None = None
    references: dict[str, Any] = field(default_factory=dict)
    character_reference_collection_ids: list[str] = field(default_factory=list)
    product_reference_collection_ids: list[str] = field(default_factory=list)
    style_reference_collection_ids: list[str] = field(default_factory=list)
    responses: dict[str, ResponseRecord] = field(default_factory=dict)
    raw: dict[str, Any] = field(default_factory=dict)
    sources: list[str] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        data = asdict(self)
        data["responses"] = [response.to_dict() for response in self.responses.values()]
        return data


class Catalog:
    """Canonical in-memory creative catalog keyed by generation request ID."""

    def __init__(self) -> None:
        self.generations: dict[str, GenerationRecord] = {}

    def ingest(self, record: GenerationRecord) -> GenerationRecord:
        existing = self.generations.get(record.request_id)
        if existing is None:
            self.generations[record.request_id] = record
            return record

        old = existing.to_dict()
        new = record.to_dict()
        preferred = new if completeness_score(new) >= completeness_score(old) else old
        fallback = old if preferred is new else new
        merged = _deep_merge(fallback, preferred)

        rebuilt = GenerationRecord(
            request_id=record.request_id,
            request_type=merged.get("request_type"),
            user_prompt=merged.get("user_prompt"),
            user_negative_prompt=merged.get("user_negative_prompt"),
            caption=merged.get("caption"),
            seed=merged.get("seed"),
            model_version=merged.get("model_version"),
            model_uri=merged.get("model_uri"),
            width=merged.get("width"),
            height=merged.get("height"),
            aspect_ratio=merged.get("aspect_ratio"),
            image_resolution=merged.get("image_resolution"),
            style_expert=merged.get("style_expert"),
            creation_time_float=merged.get("creation_time_float"),
            private=merged.get("private"),
            completed=merged.get("completed"),
            errored=merged.get("errored"),
            references=merged.get("references") or {},
            character_reference_collection_ids=merged.get("character_reference_collection_ids") or [],
            product_reference_collection_ids=merged.get("product_reference_collection_ids") or [],
            style_reference_collection_ids=merged.get("style_reference_collection_ids") or [],
            raw=_deep_merge(existing.raw, record.raw),
            sources=list(dict.fromkeys(existing.sources + record.sources)),
        )

        for response in list(existing.responses.values()) + list(record.responses.values()):
            current = rebuilt.responses.get(response.response_id)
            if current is None:
                rebuilt.responses[response.response_id] = response
                continue
            current.raw = _deep_merge(current.raw, response.raw)
            current.sources = list(dict.fromkeys(current.sources + response.sources))
            for attr in ("response_index", "prompt", "asset_url", "format", "likes", "private"):
                value = getattr(response, attr)
                if not _is_missing(value):
                    setattr(current, attr, value)

        self.generations[record.request_id] = rebuilt
        return rebuilt

    def extend(self, records: Iterable[GenerationRecord]) -> None:
        for record in records:
            self.ingest(record)

    def summary(self) -> dict[str, Any]:
        responses = sum(len(item.responses) for item in self.generations.values())
        models: dict[str, int] = {}
        request_types: dict[str, int] = {}
        for item in self.generations.values():
            if item.model_version:
                models[item.model_version] = models.get(item.model_version, 0) + 1
            if item.request_type:
                request_types[item.request_type] = request_types.get(item.request_type, 0) + 1
        return {
            "generation_count": len(self.generations),
            "response_count": responses,
            "models": dict(sorted(models.items(), key=lambda kv: (-kv[1], kv[0]))),
            "request_types": dict(sorted(request_types.items(), key=lambda kv: (-kv[1], kv[0]))),
        }
