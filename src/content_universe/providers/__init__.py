"""Live/provider execution contracts.

This namespace is deliberately separate from `content_universe.adapters`, which
contains recovery/evidence parsers. Provider modules describe supported live
state and mutation surfaces without owning the canonical Content Universe model.
"""

from .contracts import ProviderToolCatalog, ProviderToolContract

__all__ = ["ProviderToolCatalog", "ProviderToolContract"]
