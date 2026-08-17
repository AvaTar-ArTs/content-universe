from __future__ import annotations

from dataclasses import dataclass, field, asdict
from datetime import datetime, timezone
from typing import Any


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


@dataclass(slots=True)
class Observation:
    source: str
    observed_at: str = field(default_factory=utc_now)
    locator: str | None = None
    confidence: float | None = None
    metadata: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(slots=True)
class ProvenanceLedger:
    observations: dict[str, list[Observation]] = field(default_factory=dict)

    def add(self, entity_key: str, observation: Observation) -> None:
        bucket = self.observations.setdefault(entity_key, [])
        signature = (observation.source, observation.locator, observation.observed_at)
        if not any((o.source, o.locator, o.observed_at) == signature for o in bucket):
            bucket.append(observation)

    def sources_for(self, entity_key: str) -> list[str]:
        return list(dict.fromkeys(o.source for o in self.observations.get(entity_key, [])))

    def to_dict(self) -> dict[str, Any]:
        return {key: [o.to_dict() for o in values] for key, values in self.observations.items()}
