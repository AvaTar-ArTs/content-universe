from __future__ import annotations

from importlib.metadata import entry_points
from typing import Iterable

from .adapters.base import Adapter, AdapterRegistry

ENTRY_POINT_GROUP = "content_universe.adapters"


def discover_adapters(group: str = ENTRY_POINT_GROUP) -> list[Adapter]:
    """Load third-party adapters registered through Python entry points.

    An adapter package can declare:

    [project.entry-points."content_universe.adapters"]
    myplatform = "my_package:MyAdapter"
    """
    found: list[Adapter] = []
    for ep in entry_points(group=group):
        factory = ep.load()
        adapter = factory() if isinstance(factory, type) else factory
        if not isinstance(adapter, Adapter):
            raise TypeError(f"entry point {ep.name!r} did not provide an Adapter instance")
        found.append(adapter)
    return found


def register_plugins(registry: AdapterRegistry, adapters: Iterable[Adapter] | None = None) -> AdapterRegistry:
    for adapter in adapters if adapters is not None else discover_adapters():
        registry.register(adapter)
    return registry
