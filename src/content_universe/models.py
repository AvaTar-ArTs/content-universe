from __future__ import annotations

from dataclasses import asdict, dataclass, field
from enum import StrEnum
from typing import Any


class EntityKind(StrEnum):
    GENERATION = "generation"
    RESPONSE = "response"
    ASSET = "asset"
    COLLECTION = "collection"
    PROFILE = "profile"
    PROJECT = "project"
    SERIES = "series"
    STORY = "story"
    CHARACTER = "character"
    CONCEPT = "concept"
    CHAPTER = "chapter"
    SCENE = "scene"
    TRACK = "track"
    IMAGE = "image"
    VIDEO = "video"
    PROMPT = "prompt"
    PROMPT_MANIFEST = "prompt_manifest"
    SCENE_GRAPH = "scene_graph"
    STRUCTURED_DESIGN_ASSET = "structured_design_asset"
    STYLE_DNA = "style_dna"
    REFERENCE_GENOME = "reference_genome"
    EVALUATION = "evaluation"
    APPROVAL = "approval"
    WORKFLOW = "workflow"
    WORKFLOW_RUN = "workflow_run"
    SKILL_INVOCATION = "skill_invocation"
    WORKFLOW_HANDOFF = "workflow_handoff"
    CHECKPOINT = "checkpoint"
    PROVIDER_JOB = "provider_job"
    VERIFICATION = "verification"
    CUE_MAP = "cue_map"
    SHOT_MANIFEST = "shot_manifest"
    PUBLICATION = "publication"
    PRODUCT = "product"
    CAMPAIGN = "campaign"
    FILE = "file"


class EdgeKind(StrEnum):
    PRODUCED = "produced"
    EDIT_OF = "edit_of"
    VARIATION_OF = "variation_of"
    STYLE_REFERENCE = "style_reference"
    CHARACTER_REFERENCE = "character_reference"
    PRODUCT_REFERENCE = "product_reference"
    UPLOAD_PARENT = "upload_parent"
    MEMBER_OF = "member_of"
    PART_OF = "part_of"
    INSTANCE_OF = "instance_of"
    FEATURES = "features"
    DEPICTS = "depicts"
    ADAPTS = "adapts"
    INSPIRED_BY = "inspired_by"
    USES = "uses"
    PUBLISHED_AS = "published_as"
    COVER_FOR = "cover_for"
    SOUNDTRACK_FOR = "soundtrack_for"
    PROMPT_FOR = "prompt_for"
    DERIVED_FROM = "derived_from"
    EXPANDED_INTO = "expanded_into"
    RENDERED_AS = "rendered_as"
    EVALUATED_BY = "evaluated_by"
    APPROVED_AS = "approved_as"
    TRAINED_INTO = "trained_into"
    REVISION_OF = "revision_of"
    RELATED_TO = "related_to"
    SELECTED_WORKFLOW = "selected_workflow"
    INVOKED_AS = "invoked_as"
    HANDED_OFF_TO = "handed_off_to"
    CHECKPOINT_OF = "checkpoint_of"
    EXECUTED_AS = "executed_as"
    VERIFIED_BY = "verified_by"
    CUE_MAP_FOR = "cue_map_for"
    SHOT_PLAN_FOR = "shot_plan_for"
    RESUMES = "resumes"


@dataclass(slots=True, frozen=True)
class EntityRef:
    kind: EntityKind
    id: str

    @property
    def key(self) -> str:
        return f"{self.kind}:{self.id}"


@dataclass(slots=True)
class AssetRecord:
    asset_id: str
    response_id: str | None = None
    url: str | None = None
    representation: str | None = None
    resolution: str | None = None
    media_type: str | None = None
    width: int | None = None
    height: int | None = None
    metadata: dict[str, Any] = field(default_factory=dict)
    sources: list[str] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(slots=True)
class CollectionRecord:
    collection_id: str
    collection_type: str | None = None
    version_id: str | None = None
    assets: list[str] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)
    sources: list[str] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(slots=True)
class ProfileRecord:
    user_id: str | None = None
    handle: str | None = None
    generation_count: int | None = None
    likes: int | None = None
    joined_at: str | None = None
    metadata: dict[str, Any] = field(default_factory=dict)
    sources: list[str] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(slots=True)
class CreativeEntity:
    entity_id: str
    kind: EntityKind
    title: str | None = None
    description: str | None = None
    aliases: list[str] = field(default_factory=list)
    tags: list[str] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)
    sources: list[str] = field(default_factory=list)

    @property
    def ref(self) -> EntityRef:
        return EntityRef(self.kind, self.entity_id)

    def to_dict(self) -> dict[str, Any]:
        data = asdict(self)
        data["kind"] = self.kind.value
        return data
