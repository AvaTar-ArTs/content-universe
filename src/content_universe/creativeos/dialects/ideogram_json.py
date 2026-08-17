from __future__ import annotations

from typing import Any

from ...promptlab import decompose_prompt
from ..importers import prompt_manifest_from_decomposition
from ..prompt import PromptManifest
from ..scene import SceneElementKind


class IdeogramJsonDialect:
    """Portable bridge for the structured Ideogram prompt shape observed in captures.

    This class translates data only. It does not call Ideogram or claim that a
    provider accepted the exported payload. Unknown provider-specific fields are
    preserved on import inside scene-element metadata where available.
    """

    name = "ideogram_json"

    def import_payload(self, payload: Any, *, manifest_id: str) -> PromptManifest:
        if not isinstance(payload, dict):
            raise TypeError("ideogram_json payload must be an object")
        original = payload.get("original_prompt") or payload.get("user_prompt")
        structured = payload.get("structured_prompt") or payload.get("prompt") or payload
        decomposition = decompose_prompt(original, structured)
        manifest = prompt_manifest_from_decomposition(
            manifest_id,
            decomposition,
            source=self.name,
            metadata={"import_dialect": self.name},
        )
        return manifest

    def export_manifest(self, manifest: PromptManifest) -> dict[str, Any]:
        scene = manifest.scene
        if scene is None:
            raise ValueError("ideogram_json export requires a SceneGraph")

        elements: list[dict[str, Any]] = []
        for element in scene.elements:
            raw = dict(element.metadata.get("provider_raw") or {})
            if element.kind is SceneElementKind.TEXT:
                raw["type"] = "text"
                if element.text is not None:
                    raw["text"] = element.text
            elif element.kind is SceneElementKind.OBJECT:
                raw["type"] = "obj"
            else:
                raw.setdefault("type", element.kind.value)
            if element.description is not None:
                raw["desc"] = element.description
            elements.append(raw)

        structured: dict[str, Any] = {
            "high_level_description": scene.high_level_description,
            "compositional_deconstruction": {
                "background": scene.background,
                "elements": elements,
            },
        }
        return {
            "dialect": self.name,
            "original_prompt": manifest.original_prompt,
            "structured_prompt": structured,
        }

    def validate_manifest(self, manifest: PromptManifest) -> list[str]:
        errors: list[str] = []
        if manifest.scene is None:
            errors.append("ideogram_json requires a SceneGraph")
            return errors
        for element in manifest.scene.elements:
            if element.kind is SceneElementKind.TEXT and not element.text:
                errors.append(f"text element {element.element_id!r} requires exact text")
        return errors
