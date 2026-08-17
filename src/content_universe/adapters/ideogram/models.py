from __future__ import annotations

from dataclasses import dataclass, field, asdict
from typing import Any, Iterable


CAPABILITY_FIELDS = (
    "supports_inpaint",
    "supports_canvas",
    "supports_color_palette",
    "supports_negative_prompt",
    "supports_rendering_speed",
    "supports_tiling",
    "supports_style_reference",
    "supports_custom_aspect_ratio",
    "supports_character_reference",
    "supports_product_reference",
    "supports_flash_rendering_speed",
    "supports_external_api",
    "auto_background_removal",
    "is_custom_model",
    "is_primary_model",
)


@dataclass(slots=True)
class ModelRecord:
    id: str
    name: str | None = None
    uri: str | None = None
    access_level: str | None = None
    available_resolution_tiers: list[str] = field(default_factory=list)
    capabilities: dict[str, bool] = field(default_factory=dict)
    raw: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def _walk(value: Any) -> Iterable[dict[str, Any]]:
    if isinstance(value, dict):
        yield value
        for child in value.values():
            yield from _walk(child)
    elif isinstance(value, list):
        for child in value:
            yield from _walk(child)


def model_records(payload: Any) -> list[ModelRecord]:
    records: list[ModelRecord] = []
    seen: set[str] = set()
    for item in _walk(payload):
        if not any(field in item for field in CAPABILITY_FIELDS):
            continue
        model_id = item.get("model_id") or item.get("id") or item.get("model_uri") or item.get("uri")
        if not model_id:
            continue
        model_id = str(model_id)
        if model_id in seen:
            continue
        seen.add(model_id)
        capabilities = {field: bool(item.get(field)) for field in CAPABILITY_FIELDS if field in item}
        tiers = item.get("available_resolution_tiers") or item.get("resolution_tiers") or []
        records.append(ModelRecord(
            id=model_id,
            name=item.get("display_name") or item.get("name"),
            uri=item.get("model_uri") or item.get("uri"),
            access_level=item.get("access_level"),
            available_resolution_tiers=[str(v) for v in tiers] if isinstance(tiers, list) else [],
            capabilities=capabilities,
            raw=dict(item),
        ))
    return records


def filter_models(records: Iterable[ModelRecord], *, capability: str | None = None, custom: bool | None = None) -> list[ModelRecord]:
    result = list(records)
    if capability:
        result = [record for record in result if record.capabilities.get(capability) is True]
    if custom is not None:
        result = [record for record in result if record.capabilities.get("is_custom_model", False) is custom]
    return result
