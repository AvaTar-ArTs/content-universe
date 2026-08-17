from __future__ import annotations

from dataclasses import asdict, dataclass, field
from typing import Any

from ..models import EntityRef
from .operations import ReferenceBinding


@dataclass(slots=True, frozen=True)
class CuePoint:
    cue_id: str
    start_seconds: float
    end_seconds: float
    label: str
    energy: float | None = None
    lyric_or_event: str | None = None
    visual_intent: str | None = None
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        if self.start_seconds < 0:
            raise ValueError("cue start cannot be negative")
        if self.end_seconds <= self.start_seconds:
            raise ValueError("cue end must be greater than cue start")
        if self.energy is not None and not 0 <= self.energy <= 1:
            raise ValueError("cue energy must be between 0 and 1")

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(slots=True, frozen=True)
class CueMap:
    cue_map_id: str
    source_track: EntityRef
    duration_seconds: float
    cues: list[CuePoint] = field(default_factory=list)
    bpm: float | None = None
    key: str | None = None
    meter: str | None = None
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        if self.duration_seconds <= 0:
            raise ValueError("duration_seconds must be positive")
        previous_end = 0.0
        seen: set[str] = set()
        for cue in self.cues:
            if cue.cue_id in seen:
                raise ValueError(f"duplicate cue_id: {cue.cue_id}")
            seen.add(cue.cue_id)
            if cue.start_seconds < previous_end:
                raise ValueError("cues must be ordered and non-overlapping")
            if cue.end_seconds > self.duration_seconds:
                raise ValueError("cue exceeds track duration")
            previous_end = cue.end_seconds

    def to_dict(self) -> dict[str, Any]:
        return {
            "cue_map_id": self.cue_map_id,
            "source_track": _ref_to_dict(self.source_track),
            "duration_seconds": self.duration_seconds,
            "cues": [item.to_dict() for item in self.cues],
            "bpm": self.bpm,
            "key": self.key,
            "meter": self.meter,
            "metadata": self.metadata,
        }


@dataclass(slots=True, frozen=True)
class ShotSpec:
    shot_id: str
    scene_id: str
    cue_ids: list[str]
    start_seconds: float
    end_seconds: float
    framing: str | None = None
    camera: str | None = None
    action: str | None = None
    emotion: str | None = None
    location: str | None = None
    prompt_manifest_id: str | None = None
    scene_graph_id: str | None = None
    references: list[ReferenceBinding] = field(default_factory=list)
    protected_fields: dict[str, Any] = field(default_factory=dict)
    render_requirements: dict[str, Any] = field(default_factory=dict)
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        if self.start_seconds < 0:
            raise ValueError("shot start cannot be negative")
        if self.end_seconds <= self.start_seconds:
            raise ValueError("shot end must be greater than shot start")
        if not self.cue_ids:
            raise ValueError("shot must map to at least one cue")

    def to_dict(self) -> dict[str, Any]:
        return {
            "shot_id": self.shot_id,
            "scene_id": self.scene_id,
            "cue_ids": self.cue_ids,
            "start_seconds": self.start_seconds,
            "end_seconds": self.end_seconds,
            "framing": self.framing,
            "camera": self.camera,
            "action": self.action,
            "emotion": self.emotion,
            "location": self.location,
            "prompt_manifest_id": self.prompt_manifest_id,
            "scene_graph_id": self.scene_graph_id,
            "references": [item.to_dict() for item in self.references],
            "protected_fields": self.protected_fields,
            "render_requirements": self.render_requirements,
            "metadata": self.metadata,
        }


@dataclass(slots=True, frozen=True)
class ShotManifest:
    shot_manifest_id: str
    workflow_run_id: str
    cue_map_id: str
    shots: list[ShotSpec] = field(default_factory=list)
    output_requirements: dict[str, Any] = field(default_factory=dict)
    review_status: str = "pending"
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        seen: set[str] = set()
        previous_start = -1.0
        for shot in self.shots:
            if shot.shot_id in seen:
                raise ValueError(f"duplicate shot_id: {shot.shot_id}")
            seen.add(shot.shot_id)
            if shot.start_seconds < previous_start:
                raise ValueError("shots must be in timeline order")
            previous_start = shot.start_seconds

    def to_dict(self) -> dict[str, Any]:
        return {
            "shot_manifest_id": self.shot_manifest_id,
            "workflow_run_id": self.workflow_run_id,
            "cue_map_id": self.cue_map_id,
            "shots": [item.to_dict() for item in self.shots],
            "output_requirements": self.output_requirements,
            "review_status": self.review_status,
            "metadata": self.metadata,
        }


def _ref_to_dict(ref: EntityRef) -> dict[str, str]:
    return {"kind": ref.kind.value, "id": ref.id}
