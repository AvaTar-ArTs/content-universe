from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Callable, Iterable

from ..models import EntityRef
from .operations import OperationKind, OperationRequest, ReferenceBinding
from .prompt import PromptLineage, PromptManifest, PromptRevision, PromptStage
from .provider import ProviderDialect
from .scene import BoundingBox, SceneElement, SceneGraph


class ProviderOperationRequired(RuntimeError):
    """Raised when a Prompt Builder method requires a real provider capability."""

    def __init__(self, operation: OperationKind, request: OperationRequest) -> None:
        self.operation = operation
        self.request = request
        super().__init__(f"{operation.value} requires a provider backend; no provider call was performed")


@dataclass(slots=True)
class ValidationReport:
    valid: bool
    errors: list[str]
    warnings: list[str]


class PromptBuilder:
    """Local structured-authoring service.

    Local methods modify portable CreativeOS state. Provider-backed methods only
    construct explicit semantic requests; they never fabricate provider output.
    """

    def build(self, manifest_id: str, *, brief: str | None = None, prompt: str | None = None) -> PromptManifest:
        lineage = PromptLineage(original=prompt) if prompt is not None else None
        return PromptManifest(manifest_id=manifest_id, brief=brief, lineage=lineage, scene=SceneGraph())

    def import_payload(self, dialect: ProviderDialect, payload: Any, *, manifest_id: str) -> PromptManifest:
        result = dialect.import_payload(payload, manifest_id=manifest_id)
        if not isinstance(result, PromptManifest):
            raise TypeError("provider dialect import must return PromptManifest")
        return result

    def deconstruct(self, manifest: PromptManifest, scene: SceneGraph) -> PromptManifest:
        manifest.scene = scene
        return manifest

    def compose_add(self, manifest: PromptManifest, element: SceneElement) -> PromptManifest:
        if manifest.scene is None:
            manifest.scene = SceneGraph()
        manifest.scene.add_element(element)
        return manifest

    def compose_remove(self, manifest: PromptManifest, element_id: str) -> PromptManifest:
        if manifest.scene is None:
            raise ValueError("manifest has no scene graph")
        before = len(manifest.scene.elements)
        manifest.scene.elements = [item for item in manifest.scene.elements if item.element_id != element_id]
        if len(manifest.scene.elements) == before:
            raise KeyError(f"unknown scene element: {element_id}")
        return manifest

    def compose_move(self, manifest: PromptManifest, element_id: str, bounds: BoundingBox) -> PromptManifest:
        if manifest.scene is None:
            raise ValueError("manifest has no scene graph")
        element = manifest.scene.get_element(element_id)
        if element is None:
            raise KeyError(f"unknown scene element: {element_id}")
        element.bounds = bounds
        return manifest

    def reference(self, manifest: PromptManifest, reference: ReferenceBinding) -> PromptManifest:
        manifest.references.append(reference)
        return manifest

    def enhance(self, manifest: PromptManifest, value: Any, *, source: str = "local") -> PromptManifest:
        if manifest.lineage is None:
            raise ValueError("cannot enhance without an original prompt lineage")
        manifest.lineage = manifest.lineage.append(
            PromptRevision(stage=PromptStage.ENHANCED, value=value, source=source)
        )
        return manifest

    def localize(
        self,
        manifest: PromptManifest,
        text_map: dict[str, str],
        *,
        language: str | None = None,
    ) -> PromptManifest:
        if manifest.scene is None:
            raise ValueError("manifest has no scene graph")
        changed: dict[str, str] = {}
        for element in manifest.scene.elements:
            if element.text is None or element.text not in text_map:
                continue
            original = element.text
            element.text = text_map[original]
            if element.typography is not None:
                element.typography.text = element.text
            changed[original] = element.text
        if manifest.lineage is not None and changed:
            manifest.lineage = manifest.lineage.append(
                PromptRevision(
                    stage=PromptStage.LOCALIZED,
                    value={"language": language, "text_map": changed},
                    source="local",
                )
            )
        return manifest

    def reflow(
        self,
        manifest: PromptManifest,
        *,
        aspect_ratio: str | None = None,
        dimensions: tuple[int, int] | None = None,
        transform: Callable[[SceneGraph], SceneGraph] | None = None,
    ) -> PromptManifest:
        if aspect_ratio is None and dimensions is None:
            raise ValueError("reflow requires aspect_ratio or dimensions")
        if dimensions is not None and (dimensions[0] <= 0 or dimensions[1] <= 0):
            raise ValueError("reflow dimensions must be positive")
        manifest.aspect_ratio = aspect_ratio or manifest.aspect_ratio
        manifest.dimensions = dimensions or manifest.dimensions
        if transform is not None:
            if manifest.scene is None:
                raise ValueError("manifest has no scene graph")
            manifest.scene = transform(manifest.scene)
        if manifest.lineage is not None:
            manifest.lineage = manifest.lineage.append(
                PromptRevision(
                    stage=PromptStage.REFLOWED,
                    value={"aspect_ratio": aspect_ratio, "dimensions": dimensions},
                    source="local",
                )
            )
        return manifest

    def validate(self, manifest: PromptManifest, dialect: ProviderDialect | None = None) -> ValidationReport:
        errors: list[str] = []
        warnings: list[str] = []
        if not manifest.manifest_id:
            errors.append("manifest_id is required")
        if manifest.scene is not None:
            ids = [element.element_id for element in manifest.scene.elements]
            if len(ids) != len(set(ids)):
                errors.append("scene element IDs must be unique")
        if manifest.dimensions is not None and any(value <= 0 for value in manifest.dimensions):
            errors.append("dimensions must be positive")
        if dialect is not None:
            errors.extend(dialect.validate_manifest(manifest))
        if manifest.lineage is None:
            warnings.append("manifest has no original prompt lineage")
        return ValidationReport(valid=not errors, errors=errors, warnings=warnings)

    def export(self, manifest: PromptManifest, dialect: ProviderDialect) -> Any:
        report = self.validate(manifest, dialect)
        if not report.valid:
            raise ValueError("cannot export invalid prompt manifest: " + "; ".join(report.errors))
        return dialect.export_manifest(manifest)

    def describe(self, source: EntityRef) -> None:
        request = OperationRequest(OperationKind.DESCRIBE, sources=[source])
        raise ProviderOperationRequired(OperationKind.DESCRIBE, request)

    def magic_prompt(self, manifest: PromptManifest) -> None:
        request = OperationRequest(OperationKind.MAGIC_PROMPT, prompt_manifest_id=manifest.manifest_id)
        raise ProviderOperationRequired(OperationKind.MAGIC_PROMPT, request)

    def layerize_text(self, source: EntityRef) -> None:
        request = OperationRequest(OperationKind.LAYERIZE_TEXT, sources=[source])
        raise ProviderOperationRequired(OperationKind.LAYERIZE_TEXT, request)

    def edit(self, manifest: PromptManifest, sources: Iterable[EntityRef]) -> None:
        request = OperationRequest(
            OperationKind.EDIT,
            sources=list(sources),
            references=list(manifest.references),
            prompt_manifest_id=manifest.manifest_id,
        )
        raise ProviderOperationRequired(OperationKind.EDIT, request)
