from __future__ import annotations

import hashlib
import json
import tempfile
import zipfile
from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from .adapters.ideogram.assets import manifest_from_records
from .audit import audit_records
from .universe import ContentUniverse


@dataclass(slots=True)
class PackFile:
    path: str
    sha256: str
    bytes: int


@dataclass(slots=True)
class DatasetPackManifest:
    format: str
    format_version: int
    created_at: str
    summary: dict[str, Any]
    audit: dict[str, Any]
    files: list[PackFile]

    def to_dict(self) -> dict[str, Any]:
        return {
            "format": self.format,
            "format_version": self.format_version,
            "created_at": self.created_at,
            "summary": self.summary,
            "audit": self.audit,
            "files": [asdict(item) for item in self.files],
        }


def _sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _write_json(path: Path, payload: Any) -> None:
    path.write_text(json.dumps(payload, indent=2, ensure_ascii=False), encoding="utf-8")


def build_dataset_pack(universe: ContentUniverse, output: str | Path) -> Path:
    """Build a deterministic portable ZIP of normalized Content Universe data.

    The pack contains normalized data only. It never embeds raw HAR files,
    cookies, browser sessions, or downloaded media binaries.
    """
    output_path = Path(output)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    with tempfile.TemporaryDirectory(prefix="content-universe-pack-") as temp_dir:
        root = Path(temp_dir)
        records = list(universe.generations.values())

        universe_path = root / "universe.json"
        generations_path = root / "generations.jsonl"
        graph_path = root / "graph.json"
        mermaid_path = root / "graph.mmd"
        provenance_path = root / "provenance.json"
        assets_path = root / "asset-manifest.json"
        audit_path = root / "audit.json"

        _write_json(universe_path, universe.to_dict())
        with generations_path.open("w", encoding="utf-8") as handle:
            for record in records:
                handle.write(json.dumps(record.to_dict(), ensure_ascii=False) + "\n")
        _write_json(graph_path, universe.graph.to_dict())
        mermaid_path.write_text(universe.graph.to_mermaid(), encoding="utf-8")
        _write_json(provenance_path, universe.provenance.to_dict())
        _write_json(assets_path, [item.to_dict() for item in manifest_from_records(records)])
        audit = audit_records(records).to_dict()
        _write_json(audit_path, audit)

        data_files = [
            universe_path,
            generations_path,
            graph_path,
            mermaid_path,
            provenance_path,
            assets_path,
            audit_path,
        ]
        pack_files = [PackFile(path=item.name, sha256=_sha256(item), bytes=item.stat().st_size) for item in data_files]
        manifest = DatasetPackManifest(
            format="content-universe-dataset-pack",
            format_version=1,
            created_at=datetime.now(timezone.utc).isoformat(),
            summary=universe.summary(),
            audit=audit,
            files=pack_files,
        )
        manifest_path = root / "pack.json"
        _write_json(manifest_path, manifest.to_dict())

        with zipfile.ZipFile(output_path, "w", compression=zipfile.ZIP_DEFLATED) as archive:
            archive.write(manifest_path, manifest_path.name)
            for item in data_files:
                archive.write(item, item.name)

    return output_path
