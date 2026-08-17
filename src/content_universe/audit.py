from __future__ import annotations

from collections import Counter
from dataclasses import dataclass, field, asdict
from statistics import mean
from typing import Any, Iterable

from .catalog import GenerationRecord, completeness_score


IMPORTANT_GENERATION_FIELDS = (
    "request_type",
    "user_prompt",
    "seed",
    "model_version",
    "aspect_ratio",
    "image_resolution",
)


@dataclass(slots=True)
class AuditReport:
    generation_count: int = 0
    response_count: int = 0
    generations_without_responses: int = 0
    average_completeness: float = 0.0
    minimum_completeness: int = 0
    maximum_completeness: int = 0
    missing_fields: dict[str, int] = field(default_factory=dict)
    model_counts: dict[str, int] = field(default_factory=dict)
    request_type_counts: dict[str, int] = field(default_factory=dict)
    response_count_distribution: dict[int, int] = field(default_factory=dict)
    source_counts: dict[str, int] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def audit_records(records: Iterable[GenerationRecord]) -> AuditReport:
    items = list(records)
    scores = [completeness_score(item.to_dict()) for item in items]
    missing = Counter()
    models = Counter()
    request_types = Counter()
    response_distribution = Counter()
    sources = Counter()

    for item in items:
        for field_name in IMPORTANT_GENERATION_FIELDS:
            value = getattr(item, field_name)
            if value in (None, "", [], {}):
                missing[field_name] += 1
        models[item.model_version or "<unknown>"] += 1
        request_types[item.request_type or "<unknown>"] += 1
        response_distribution[len(item.responses)] += 1
        for source in item.sources:
            sources[source] += 1

    return AuditReport(
        generation_count=len(items),
        response_count=sum(len(item.responses) for item in items),
        generations_without_responses=sum(1 for item in items if not item.responses),
        average_completeness=round(mean(scores), 2) if scores else 0.0,
        minimum_completeness=min(scores) if scores else 0,
        maximum_completeness=max(scores) if scores else 0,
        missing_fields=dict(sorted(missing.items(), key=lambda kv: (-kv[1], kv[0]))),
        model_counts=dict(models.most_common()),
        request_type_counts=dict(request_types.most_common()),
        response_count_distribution=dict(sorted(response_distribution.items())),
        source_counts=dict(sources.most_common()),
    )
