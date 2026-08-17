from __future__ import annotations

from dataclasses import asdict, dataclass, field
from enum import StrEnum
from typing import Any

from ..models import EntityRef


class OperationKind(StrEnum):
    """Provider-neutral creative intent.

    These values are intentionally distinct. A backend must not silently execute
    a different operation merely because another provider primitive is available.
    """

    GENERATE = "generate"
    EDIT = "edit"
    REMIX = "remix"
    REFRAME = "reframe"
    UPSCALE = "upscale"
    REMOVE_BACKGROUND = "remove_background"
    DESCRIBE = "describe"
    LAYERIZE_TEXT = "layerize_text"


class ExecutionMode(StrEnum):
    LOCAL = "local"
    MOCK = "mock"
    PROVIDER = "provider"


class ReferenceRole(StrEnum):
    """Why a reference exists in the authoring/runtime system."""

    AUTHORING = "authoring"
    GENERATION = "generation"
    EVALUATION = "evaluation"
    CONTINUITY = "continuity"


class ReferenceKind(StrEnum):
    IMAGE = "image"
    CHARACTER = "character"
    STYLE = "style"
    COMPOSITION = "composition"
    PRODUCT = "product"
    TYPOGRAPHY = "typography"
    PALETTE = "palette"
    CUSTOM_MODEL = "custom_model"
    OTHER = "other"


@dataclass(slots=True, frozen=True)
class ReferenceBinding:
    """A reference with explicit role and semantic kind.

    `ref` points into Content Universe when the referenced object is already
    canonical. `locator` permits an external/local reference before ingestion.
    At least one must be present.
    """

    role: ReferenceRole
    kind: ReferenceKind
    ref: EntityRef | None = None
    locator: str | None = None
    weight: float | None = None
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        if self.ref is None and not self.locator:
            raise ValueError("reference requires a canonical ref or locator")
        if self.weight is not None and self.weight < 0:
            raise ValueError("reference weight cannot be negative")

    def to_dict(self) -> dict[str, Any]:
        data = asdict(self)
        data["role"] = self.role.value
        data["kind"] = self.kind.value
        if self.ref is not None:
            data["ref"] = {"kind": self.ref.kind.value, "id": self.ref.id}
        return data


_EXACTLY_ONE_SOURCE = {
    OperationKind.REMIX,
    OperationKind.REFRAME,
    OperationKind.UPSCALE,
    OperationKind.REMOVE_BACKGROUND,
    OperationKind.DESCRIBE,
    OperationKind.LAYERIZE_TEXT,
}

_AT_LEAST_ONE_SOURCE = {
    OperationKind.EDIT,
}

_NO_SOURCE = {
    OperationKind.GENERATE,
}


@dataclass(slots=True)
class OperationRequest:
    operation: OperationKind
    sources: list[EntityRef] = field(default_factory=list)
    references: list[ReferenceBinding] = field(default_factory=list)
    prompt_manifest_id: str | None = None
    parameters: dict[str, Any] = field(default_factory=dict)
    privacy: str | None = None
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        self.validate()

    def validate(self) -> None:
        count = len(self.sources)
        if self.operation in _NO_SOURCE and count:
            raise ValueError(f"{self.operation.value} does not accept source assets; use references for conditioning")
        if self.operation in _EXACTLY_ONE_SOURCE and count != 1:
            raise ValueError(f"{self.operation.value} requires exactly one source asset")
        if self.operation in _AT_LEAST_ONE_SOURCE and count < 1:
            raise ValueError(f"{self.operation.value} requires at least one source asset")

    @property
    def generation_references(self) -> list[ReferenceBinding]:
        """Only references explicitly authorized for provider conditioning."""

        return [item for item in self.references if item.role is ReferenceRole.GENERATION]

    def to_dict(self) -> dict[str, Any]:
        return {
            "operation": self.operation.value,
            "sources": [{"kind": item.kind.value, "id": item.id} for item in self.sources],
            "references": [item.to_dict() for item in self.references],
            "prompt_manifest_id": self.prompt_manifest_id,
            "parameters": self.parameters,
            "privacy": self.privacy,
            "metadata": self.metadata,
        }


@dataclass(slots=True)
class OperationResult:
    requested_operation: OperationKind
    executed_operation: OperationKind
    execution_mode: ExecutionMode
    provider: str | None = None
    provider_call_performed: bool = False
    job_id: str | None = None
    outputs: list[EntityRef] = field(default_factory=list)
    raw: dict[str, Any] = field(default_factory=dict)
    warnings: list[str] = field(default_factory=list)

    def __post_init__(self) -> None:
        if self.executed_operation is not self.requested_operation:
            raise ValueError(
                "semantic operation substitution is forbidden; create a new explicit request for a different operation"
            )
        if self.execution_mode is ExecutionMode.PROVIDER and not self.provider_call_performed:
            raise ValueError("provider execution mode requires provider_call_performed=True")
        if self.execution_mode is not ExecutionMode.PROVIDER and self.provider_call_performed:
            raise ValueError("mock/local results cannot claim that a provider call was performed")

    def to_dict(self) -> dict[str, Any]:
        return {
            "requested_operation": self.requested_operation.value,
            "executed_operation": self.executed_operation.value,
            "execution_mode": self.execution_mode.value,
            "provider": self.provider,
            "provider_call_performed": self.provider_call_performed,
            "job_id": self.job_id,
            "outputs": [{"kind": item.kind.value, "id": item.id} for item in self.outputs],
            "raw": self.raw,
            "warnings": self.warnings,
        }
