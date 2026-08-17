"""Provider-neutral CreativeOS authoring and execution contracts.

This package intentionally sits beside the recovery adapters. Recovery adapters
parse existing evidence; CreativeOS contracts describe creator intent, structured
authoring state, semantic operations, provider capabilities, and evaluation.
"""

from .genome import ReferenceGenome, ReferenceGenomeEntry
from .operations import (
    ExecutionMode,
    OperationKind,
    OperationRequest,
    OperationResult,
    ReferenceBinding,
    ReferenceKind,
    ReferenceRole,
)
from .prompt import PromptLineage, PromptManifest, PromptRevision, PromptStage
from .provider import (
    DeterministicMockBackend,
    ProviderBackend,
    ProviderCapabilities,
    ProviderRegistry,
)
from .scene import (
    BoundingBox,
    SceneElement,
    SceneElementKind,
    SceneGraph,
    TypographyLayer,
)
from .style import StyleDNA, StyleLayer, StyleSourceKind, StyleStack

__all__ = [
    "BoundingBox",
    "DeterministicMockBackend",
    "ExecutionMode",
    "OperationKind",
    "OperationRequest",
    "OperationResult",
    "PromptLineage",
    "PromptManifest",
    "PromptRevision",
    "PromptStage",
    "ProviderBackend",
    "ProviderCapabilities",
    "ProviderRegistry",
    "ReferenceBinding",
    "ReferenceGenome",
    "ReferenceGenomeEntry",
    "ReferenceKind",
    "ReferenceRole",
    "SceneElement",
    "SceneElementKind",
    "SceneGraph",
    "StyleDNA",
    "StyleLayer",
    "StyleSourceKind",
    "StyleStack",
    "TypographyLayer",
]
