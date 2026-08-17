from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable

from ..creativeos.operations import OperationKind


@dataclass(slots=True, frozen=True)
class ProviderToolContract:
    name: str
    family: str
    mutating: bool = True
    destructive: bool = False
    semantic_operation: OperationKind | None = None
    description: str = ""


class ProviderToolCatalog:
    def __init__(self, tools: Iterable[ProviderToolContract]) -> None:
        self._tools = tuple(tools)
        names = [tool.name for tool in self._tools]
        if len(names) != len(set(names)):
            raise ValueError("provider tool names must be unique")
        self._index = {tool.name: tool for tool in self._tools}

    def get(self, name: str) -> ProviderToolContract:
        try:
            return self._index[name]
        except KeyError as exc:
            raise KeyError(f"unknown provider tool contract: {name}") from exc

    def by_family(self, family: str) -> tuple[ProviderToolContract, ...]:
        return tuple(tool for tool in self._tools if tool.family == family)

    def by_operation(self, operation: OperationKind) -> tuple[ProviderToolContract, ...]:
        return tuple(tool for tool in self._tools if tool.semantic_operation is operation)

    def mutating(self) -> tuple[ProviderToolContract, ...]:
        return tuple(tool for tool in self._tools if tool.mutating)

    def destructive(self) -> tuple[ProviderToolContract, ...]:
        return tuple(tool for tool in self._tools if tool.destructive)

    def names(self) -> tuple[str, ...]:
        return tuple(tool.name for tool in self._tools)

    def __iter__(self):
        return iter(self._tools)

    def __len__(self) -> int:
        return len(self._tools)
