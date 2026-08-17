from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

from ..catalog import GenerationRecord
from ..graph import CreativeGraph
from ..provenance import ProvenanceLedger


@dataclass(slots=True)
class HarvestResult:
    records: list[GenerationRecord] = field(default_factory=list)
    graph: CreativeGraph = field(default_factory=CreativeGraph)
    provenance: ProvenanceLedger = field(default_factory=ProvenanceLedger)
    metadata: dict[str, Any] = field(default_factory=dict)
    warnings: list[str] = field(default_factory=list)


class Adapter(ABC):
    name: str

    @abstractmethod
    def supports(self, source: str | Path) -> bool:
        raise NotImplementedError

    @abstractmethod
    def harvest(self, source: str | Path) -> HarvestResult:
        raise NotImplementedError


class AdapterRegistry:
    def __init__(self) -> None:
        self._adapters: list[Adapter] = []

    def register(self, adapter: Adapter) -> None:
        self._adapters.append(adapter)

    @property
    def adapters(self) -> tuple[Adapter, ...]:
        return tuple(self._adapters)

    def resolve(self, source: str | Path) -> Adapter:
        for adapter in self._adapters:
            if adapter.supports(source):
                return adapter
        raise ValueError(f"No adapter recognized source: {source}")

    def harvest(self, source: str | Path) -> HarvestResult:
        return self.resolve(source).harvest(source)
