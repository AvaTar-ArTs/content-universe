from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass, field
from typing import Any, Protocol

from ..models import EntityKind, EntityRef
from .operations import ExecutionMode, OperationKind, OperationRequest, OperationResult


@dataclass(slots=True)
class ProviderCapabilities:
    provider: str
    operations: set[OperationKind] = field(default_factory=set)
    models: list[str] = field(default_factory=list)
    features: dict[str, bool] = field(default_factory=dict)
    constraints: dict[str, Any] = field(default_factory=dict)
    metadata: dict[str, Any] = field(default_factory=dict)

    def supports(self, operation: OperationKind) -> bool:
        return operation in self.operations

    def to_dict(self) -> dict[str, Any]:
        return {
            "provider": self.provider,
            "operations": sorted(item.value for item in self.operations),
            "models": self.models,
            "features": self.features,
            "constraints": self.constraints,
            "metadata": self.metadata,
        }


class ProviderDialect(Protocol):
    """Reversible structured-authoring translation boundary.

    A dialect translates provider-neutral CreativeOS state to/from a provider or
    interchange representation. It must not perform provider network calls.
    """

    name: str

    def import_payload(self, payload: Any, *, manifest_id: str) -> Any:
        ...

    def export_manifest(self, manifest: Any) -> Any:
        ...

    def validate_manifest(self, manifest: Any) -> list[str]:
        ...


class ProviderBackend(Protocol):
    """Live/mock execution boundary, distinct from recovery adapters and dialects."""

    name: str

    def capabilities(self) -> ProviderCapabilities:
        ...

    def execute(self, request: OperationRequest) -> OperationResult:
        ...

    def status(self, job_id: str) -> dict[str, Any]:
        ...


class ProviderRegistry:
    def __init__(self) -> None:
        self._providers: dict[str, ProviderBackend] = {}

    def register(self, backend: ProviderBackend) -> None:
        if backend.name in self._providers:
            raise ValueError(f"provider backend already registered: {backend.name}")
        self._providers[backend.name] = backend

    def get(self, name: str) -> ProviderBackend:
        try:
            return self._providers[name]
        except KeyError as exc:
            raise KeyError(f"unknown provider backend: {name}") from exc

    def supporting(self, operation: OperationKind) -> list[ProviderBackend]:
        return [
            backend
            for backend in self._providers.values()
            if backend.capabilities().supports(operation)
        ]

    def names(self) -> list[str]:
        return sorted(self._providers)


class DeterministicMockBackend:
    """Credit-free semantic test backend.

    It deliberately reports `ExecutionMode.MOCK` and `provider_call_performed=False`
    so tests and agent surfaces cannot confuse simulated execution with a provider call.
    """

    name = "mock"

    def __init__(self, operations: set[OperationKind] | None = None) -> None:
        self._operations = operations or set(OperationKind)
        self._jobs: dict[str, dict[str, Any]] = {}

    def capabilities(self) -> ProviderCapabilities:
        return ProviderCapabilities(
            provider=self.name,
            operations=set(self._operations),
            metadata={"execution_mode": ExecutionMode.MOCK.value},
        )

    def execute(self, request: OperationRequest) -> OperationResult:
        request.validate()
        if request.operation not in self._operations:
            raise ValueError(f"mock backend does not support {request.operation.value}")

        payload = json.dumps(request.to_dict(), sort_keys=True, separators=(",", ":"), default=str)
        digest = hashlib.sha256(payload.encode("utf-8")).hexdigest()[:20]
        job_id = f"mock-{digest}"
        output = EntityRef(EntityKind.ASSET, f"mock-{request.operation.value}-{digest}")
        self._jobs[job_id] = {
            "status": "completed",
            "operation": request.operation.value,
            "output": output.key,
        }
        return OperationResult(
            requested_operation=request.operation,
            executed_operation=request.operation,
            execution_mode=ExecutionMode.MOCK,
            provider=self.name,
            provider_call_performed=False,
            job_id=job_id,
            outputs=[output],
            raw={"mock": True, "request_digest": digest},
        )

    def status(self, job_id: str) -> dict[str, Any]:
        try:
            return dict(self._jobs[job_id])
        except KeyError as exc:
            raise KeyError(f"unknown mock job: {job_id}") from exc
