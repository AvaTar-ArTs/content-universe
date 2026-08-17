"""Provider-neutral CreativeOS authoring and execution contracts.

This package intentionally sits beside the recovery adapters. Recovery adapters
parse existing evidence; CreativeOS contracts describe creator intent, structured
authoring state, semantic operations, provider capabilities, evaluation, and
reusable creative memory.
"""

from .evaluation import ApprovalRecord, ApprovalStatus, EvaluationKind, EvaluationRecord
from .genome import ReferenceGenome, ReferenceGenomeEntry
from .importers import prompt_manifest_from_decomposition, scene_graph_from_prompt_decomposition
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
    "ApprovalRecord",
    "ApprovalStatus",
    "BoundingBox",
    "DeterministicMockBackend",
    "EvaluationKind",
    "EvaluationRecord",
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
    "prompt_manifest_from_decomposition",
    "scene_graph_from_prompt_decomposition",
]
