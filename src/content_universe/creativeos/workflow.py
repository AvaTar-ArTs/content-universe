from __future__ import annotations

from dataclasses import asdict, dataclass, field
from enum import StrEnum
from typing import Any

from ..models import EntityRef
from .operations import ExecutionMode, OperationKind, OperationResult


class WorkflowRunStatus(StrEnum):
    PLANNED = "planned"
    RUNNING = "running"
    BLOCKED = "blocked"
    PARTIAL = "partial"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"


class CheckpointStatus(StrEnum):
    READY = "ready"
    RUNNING = "running"
    BLOCKED = "blocked"
    PARTIAL = "partial"
    COMPLETED = "completed"
    FAILED = "failed"


class ProviderJobStatus(StrEnum):
    QUEUED = "queued"
    RUNNING = "running"
    PARTIAL = "partial"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"
    UNKNOWN = "unknown"


class VerificationStatus(StrEnum):
    PASS = "pass"
    FAIL = "fail"
    PARTIAL = "partial"
    UNVERIFIED = "unverified"


@dataclass(slots=True, frozen=True)
class SkillInvocationRecord:
    invocation_id: str
    skill_name: str
    skill_version: str | None = None
    semantic_capability: str | None = None
    selected_workflow: str | None = None
    tool_or_mcp: str | None = None
    provider_or_backend: str | None = None
    inputs: list[EntityRef] = field(default_factory=list)
    outputs: list[EntityRef] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        data = asdict(self)
        data["inputs"] = [_ref_to_dict(item) for item in self.inputs]
        data["outputs"] = [_ref_to_dict(item) for item in self.outputs]
        return data


@dataclass(slots=True, frozen=True)
class WorkflowHandoff:
    handoff_id: str
    from_skill: str
    to_skill: str
    workflow_name: str | None = None
    approved_design: EntityRef | None = None
    inputs: list[EntityRef] = field(default_factory=list)
    outputs: list[EntityRef] = field(default_factory=list)
    assumptions: list[str] = field(default_factory=list)
    unresolved: list[str] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        data = asdict(self)
        data["approved_design"] = _optional_ref_to_dict(self.approved_design)
        data["inputs"] = [_ref_to_dict(item) for item in self.inputs]
        data["outputs"] = [_ref_to_dict(item) for item in self.outputs]
        return data


@dataclass(slots=True, frozen=True)
class WorkflowCheckpoint:
    checkpoint_id: str
    workflow_run_id: str
    phase: str
    status: CheckpointStatus = CheckpointStatus.READY
    completed_steps: list[str] = field(default_factory=list)
    artifacts: list[EntityRef] = field(default_factory=list)
    unresolved: list[str] = field(default_factory=list)
    resumable: bool = True
    metadata: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        data = asdict(self)
        data["status"] = self.status.value
        data["artifacts"] = [_ref_to_dict(item) for item in self.artifacts]
        return data


@dataclass(slots=True, frozen=True)
class ProviderJobRecord:
    job_id: str
    workflow_run_id: str
    requested_operation: OperationKind
    executed_operation: OperationKind
    execution_mode: ExecutionMode
    status: ProviderJobStatus = ProviderJobStatus.UNKNOWN
    provider: str | None = None
    provider_call_performed: bool = False
    checkpoint_id: str | None = None
    inputs: list[EntityRef] = field(default_factory=list)
    outputs: list[EntityRef] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)
    raw: dict[str, Any] = field(default_factory=dict)
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        if self.executed_operation is not self.requested_operation:
            raise ValueError("provider job cannot silently substitute semantic operations")
        if self.execution_mode is ExecutionMode.PROVIDER and not self.provider_call_performed:
            raise ValueError("provider jobs require provider_call_performed=True in provider mode")
        if self.execution_mode is not ExecutionMode.PROVIDER and self.provider_call_performed:
            raise ValueError("local/mock jobs cannot claim provider execution")

    @classmethod
    def from_operation_result(
        cls,
        *,
        workflow_run_id: str,
        result: OperationResult,
        status: ProviderJobStatus = ProviderJobStatus.COMPLETED,
        checkpoint_id: str | None = None,
        inputs: list[EntityRef] | None = None,
        metadata: dict[str, Any] | None = None,
    ) -> "ProviderJobRecord":
        if not result.job_id:
            raise ValueError("operation result requires job_id to become a durable provider job")
        return cls(
            job_id=result.job_id,
            workflow_run_id=workflow_run_id,
            requested_operation=result.requested_operation,
            executed_operation=result.executed_operation,
            execution_mode=result.execution_mode,
            status=status,
            provider=result.provider,
            provider_call_performed=result.provider_call_performed,
            checkpoint_id=checkpoint_id,
            inputs=list(inputs or []),
            outputs=list(result.outputs),
            warnings=list(result.warnings),
            raw=dict(result.raw),
            metadata=dict(metadata or {}),
        )

    def to_dict(self) -> dict[str, Any]:
        return {
            "job_id": self.job_id,
            "workflow_run_id": self.workflow_run_id,
            "requested_operation": self.requested_operation.value,
            "executed_operation": self.executed_operation.value,
            "execution_mode": self.execution_mode.value,
            "status": self.status.value,
            "provider": self.provider,
            "provider_call_performed": self.provider_call_performed,
            "checkpoint_id": self.checkpoint_id,
            "inputs": [_ref_to_dict(item) for item in self.inputs],
            "outputs": [_ref_to_dict(item) for item in self.outputs],
            "warnings": self.warnings,
            "raw": self.raw,
            "metadata": self.metadata,
        }


@dataclass(slots=True, frozen=True)
class VerificationRecord:
    verification_id: str
    workflow_run_id: str
    subject: EntityRef
    claim: str
    status: VerificationStatus = VerificationStatus.UNVERIFIED
    verification_type: str | None = None
    evidence: list[EntityRef] = field(default_factory=list)
    verifier: str | None = None
    notes: list[str] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        if self.status is VerificationStatus.PASS and not self.evidence:
            raise ValueError("passing verification requires durable evidence")

    def to_dict(self) -> dict[str, Any]:
        data = asdict(self)
        data["subject"] = _ref_to_dict(self.subject)
        data["status"] = self.status.value
        data["evidence"] = [_ref_to_dict(item) for item in self.evidence]
        return data


@dataclass(slots=True, frozen=True)
class WorkflowRun:
    workflow_run_id: str
    workflow_name: str
    status: WorkflowRunStatus = WorkflowRunStatus.PLANNED
    parent_run_id: str | None = None
    skill_invocations: list[SkillInvocationRecord] = field(default_factory=list)
    handoff_ids: list[str] = field(default_factory=list)
    checkpoint_ids: list[str] = field(default_factory=list)
    provider_job_ids: list[str] = field(default_factory=list)
    verification_ids: list[str] = field(default_factory=list)
    inputs: list[EntityRef] = field(default_factory=list)
    outputs: list[EntityRef] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return {
            "workflow_run_id": self.workflow_run_id,
            "workflow_name": self.workflow_name,
            "status": self.status.value,
            "parent_run_id": self.parent_run_id,
            "skill_invocations": [item.to_dict() for item in self.skill_invocations],
            "handoff_ids": self.handoff_ids,
            "checkpoint_ids": self.checkpoint_ids,
            "provider_job_ids": self.provider_job_ids,
            "verification_ids": self.verification_ids,
            "inputs": [_ref_to_dict(item) for item in self.inputs],
            "outputs": [_ref_to_dict(item) for item in self.outputs],
            "metadata": self.metadata,
        }


def _ref_to_dict(ref: EntityRef) -> dict[str, str]:
    return {"kind": ref.kind.value, "id": ref.id}


def _optional_ref_to_dict(ref: EntityRef | None) -> dict[str, str] | None:
    return _ref_to_dict(ref) if ref is not None else None
