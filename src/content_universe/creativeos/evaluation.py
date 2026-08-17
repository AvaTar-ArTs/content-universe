from __future__ import annotations

from dataclasses import dataclass, field
from enum import StrEnum
from typing import Any

from ..models import EntityRef
from .operations import ReferenceBinding


class EvaluationKind(StrEnum):
    CHARACTER_CONSISTENCY = "character_consistency"
    STYLE_CONSISTENCY = "style_consistency"
    TEXT_ACCURACY = "text_accuracy"
    LAYOUT_COMPLIANCE = "layout_compliance"
    CONTINUITY = "continuity"
    QUALITY = "quality"
    DUPLICATE_SIMILARITY = "duplicate_similarity"
    CUSTOM = "custom"


class ApprovalStatus(StrEnum):
    PENDING = "pending"
    APPROVED = "approved"
    REJECTED = "rejected"
    REVISION_REQUESTED = "revision_requested"


@dataclass(slots=True)
class EvaluationRecord:
    evaluation_id: str
    subject: EntityRef
    kind: EvaluationKind
    score: float | None = None
    criteria: dict[str, Any] = field(default_factory=dict)
    reasons: list[str] = field(default_factory=list)
    references: list[ReferenceBinding] = field(default_factory=list)
    evaluator: str | None = None
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        if self.score is not None and not 0 <= self.score <= 1:
            raise ValueError("evaluation score must be between 0 and 1")

    def to_dict(self) -> dict[str, Any]:
        return {
            "evaluation_id": self.evaluation_id,
            "subject": {"kind": self.subject.kind.value, "id": self.subject.id},
            "kind": self.kind.value,
            "score": self.score,
            "criteria": self.criteria,
            "reasons": self.reasons,
            "references": [item.to_dict() for item in self.references],
            "evaluator": self.evaluator,
            "metadata": self.metadata,
        }


@dataclass(slots=True)
class ApprovalRecord:
    approval_id: str
    subject: EntityRef
    status: ApprovalStatus = ApprovalStatus.PENDING
    reviewer: str | None = None
    evaluation_ids: list[str] = field(default_factory=list)
    notes: str | None = None
    metadata: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return {
            "approval_id": self.approval_id,
            "subject": {"kind": self.subject.kind.value, "id": self.subject.id},
            "status": self.status.value,
            "reviewer": self.reviewer,
            "evaluation_ids": self.evaluation_ids,
            "notes": self.notes,
            "metadata": self.metadata,
        }
