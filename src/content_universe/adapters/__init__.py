from .base import Adapter, AdapterRegistry, HarvestResult
from .ideogram.browser_export import IdeogramBrowserExportAdapter
from .ideogram.har import IdeogramHarAdapter
from .ideogram.html import IdeogramHtmlAdapter
from .suno.csv import SunoCsvAdapter
from .suno.export import SunoExportAdapter
from .suno.html import SunoHtmlAdapter


def default_registry(*, include_plugins: bool = False) -> AdapterRegistry:
    registry = AdapterRegistry()
    registry.register(IdeogramHarAdapter())
    registry.register(IdeogramHtmlAdapter())
    registry.register(IdeogramBrowserExportAdapter())
    registry.register(SunoHtmlAdapter())
    registry.register(SunoCsvAdapter())
    registry.register(SunoExportAdapter())
    if include_plugins:
        from ..plugins import register_plugins

        register_plugins(registry)
    return registry


__all__ = [
    "Adapter",
    "AdapterRegistry",
    "HarvestResult",
    "IdeogramBrowserExportAdapter",
    "IdeogramHarAdapter",
    "IdeogramHtmlAdapter",
    "SunoCsvAdapter",
    "SunoExportAdapter",
    "SunoHtmlAdapter",
    "default_registry",
]
