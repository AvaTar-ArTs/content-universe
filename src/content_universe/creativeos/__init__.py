"""Provider-neutral CreativeOS authoring and execution contracts.

This package intentionally sits beside the recovery adapters. Recovery adapters
parse existing evidence; CreativeOS contracts describe creator intent, structured
authoring state, semantic operations, provider capabilities, evaluation, reusable
creative memory, workflow provenance, resumable checkpoints, and audiovisual
planning state.
"""

from .audiovisual import CueMap, CuePoint, ShotManifest, ShotSpec
from .bridge import (
    persist_approval,
    persist_cue_map,
    persist_evaluation,
    persist_prompt_manifest,
    persist_provider_job,
    persist_reference_genome,
    persist_scene_graph,
    persist_shot_manifest,
    persist_skill_invocation,
    persist_structured_design_asset,
    persist_style_dna,
    persist_verification,
    persist_workflow_checkpoint,
    persist_workflow_handoff,
    persist_workflow_run,
)
from .design_asset import GenerationWindow, Mask, StructuredDesignAsset
from .dialects import IdeogramJsonDialect
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
from .prompt_builder import PromptBuilder, ProviderOperationRequired, ValidationReport
from .provider import (
    DeterministicMockBackend,
    ProviderBackend,
    ProviderCapabilities,
    ProviderDialect,
    ProviderRegistry,
)
from .scene import BoundingBox, SceneElement, SceneElementKind, SceneGraph, TypographyLayer
from .style import StyleDNA, StyleLayer, StyleSourceKind, StyleStack
from .workflow import (
    CheckpointStatus,
    ProviderJobRecord,
    ProviderJobStatus,
    SkillInvocationRecord,
    VerificationRecord,
    VerificationStatus,
    WorkflowCheckpoint,
    WorkflowHandoff,
    WorkflowRun,
    WorkflowRunStatus,
)

__all__ = [
    "ApprovalRecord",
    "ApprovalStatus",
    "BoundingBox",
    "CheckpointStatus",
    "CueMap",
    "CuePoint",
    "DeterministicMockBackend",
    "EvaluationKind",
    "EvaluationRecord",
    "ExecutionMode",
    "GenerationWindow",
    "IdeogramJsonDialect",
    "Mask",
    "OperationKind",
    "OperationRequest",
    "OperationResult",
    "PromptBuilder",
    "PromptLineage",
    "PromptManifest",
    "PromptRevision",
    "PromptStage",
    "ProviderBackend",
    "ProviderCapabilities",
    "ProviderDialect",
    "ProviderJobRecord",
    "ProviderJobStatus",
    "ProviderOperationRequired",
    "ProviderRegistry",
    "ReferenceBinding",
    "ReferenceGenome",
    "ReferenceGenomeEntry",
    "ReferenceKind",
    "ReferenceRole",
    "SceneElement",
    "SceneElementKind",
    "SceneGraph",
    "ShotManifest",
    "ShotSpec",
    "SkillInvocationRecord",
    "StructuredDesignAsset",
    "StyleDNA",
    "StyleLayer",
    "StyleSourceKind",
    "StyleStack",
    "TypographyLayer",
    "ValidationReport",
    "VerificationRecord",
    "VerificationStatus",
    "WorkflowCheckpoint",
    "WorkflowHandoff",
    "WorkflowRun",
    "WorkflowRunStatus",
    "persist_approval",
    "persist_cue_map",
    "persist_evaluation",
    "persist_prompt_manifest",
    "persist_provider_job",
    "persist_reference_genome",
    "persist_scene_graph",
    "persist_shot_manifest",
    "persist_skill_invocation",
    "persist_structured_design_asset",
    "persist_style_dna",
    "persist_verification",
    "persist_workflow_checkpoint",
    "persist_workflow_handoff",
    "persist_workflow_run",
    "prompt_manifest_from_decomposition",
    "scene_graph_from_prompt_decomposition",
]
