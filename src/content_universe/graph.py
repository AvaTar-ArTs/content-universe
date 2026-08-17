from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Iterable

from .models import EdgeKind, EntityRef


@dataclass(slots=True, frozen=True)
class GraphEdge:
    source: EntityRef
    target: EntityRef
    kind: EdgeKind
    metadata: dict[str, Any] = field(default_factory=dict, compare=False)
    edge_id: str | None = field(default=None, compare=False)

    @property
    def identity_key(self) -> tuple[str, str, str, str]:
        """Stable edge identity while preserving historical dedupe by default.

        Ordinary relationships omit `edge_id` and still deduplicate by
        source/target/kind. Instance-like relationships may supply an edge ID,
        such as a SceneElement ID, so multiple appearances of the same canonical
        entity are retained independently.
        """

        return (self.source.key, self.target.key, self.kind.value, self.edge_id or "")

    def to_dict(self) -> dict[str, Any]:
        return {
            "source": self.source.key,
            "target": self.target.key,
            "kind": self.kind.value,
            "edge_id": self.edge_id,
            "metadata": self.metadata,
        }


class CreativeGraph:
    def __init__(self) -> None:
        self.edges: list[GraphEdge] = []
        self._keys: set[tuple[str, str, str, str]] = set()

    def add(self, edge: GraphEdge) -> None:
        key = edge.identity_key
        if key not in self._keys:
            self._keys.add(key)
            self.edges.append(edge)

    def extend(self, edges: Iterable[GraphEdge]) -> None:
        for edge in edges:
            self.add(edge)

    def neighbors(self, ref: EntityRef, direction: str = "both") -> list[GraphEdge]:
        if direction == "out":
            return [e for e in self.edges if e.source == ref]
        if direction == "in":
            return [e for e in self.edges if e.target == ref]
        return [e for e in self.edges if e.source == ref or e.target == ref]

    def to_dict(self) -> dict[str, Any]:
        return {"edges": [edge.to_dict() for edge in self.edges]}

    def to_mermaid(self) -> str:
        lines = ["graph LR"]
        for edge in self.edges:
            a = edge.source.key.replace(":", "_").replace("-", "_")
            b = edge.target.key.replace(":", "_").replace("-", "_")
            label = edge.kind.value if edge.edge_id is None else f"{edge.kind.value}:{edge.edge_id}"
            lines.append(f'  {a}["{edge.source.key}"] -->|{label}| {b}["{edge.target.key}"]')
        return "\n".join(lines)
