"""Ideogram/iDeoMine provider-state contracts.

No live transport is implemented here. This package preserves the historical
provider surface and semantic mappings while authentication/transport remain a
future backend concern.
"""

from .contracts import IDEOGRAM_TOOL_CATALOG, IDEOGRAM_TOOL_CONTRACTS

__all__ = ["IDEOGRAM_TOOL_CATALOG", "IDEOGRAM_TOOL_CONTRACTS"]
