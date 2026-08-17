from __future__ import annotations

import csv
import json
from pathlib import Path
from typing import Iterable

from .catalog import GenerationRecord


def export_jsonl(records: Iterable[GenerationRecord], path: str | Path) -> Path:
    out = Path(path)
    out.parent.mkdir(parents=True, exist_ok=True)
    with out.open("w", encoding="utf-8") as fh:
        for record in records:
            fh.write(json.dumps(record.to_dict(), ensure_ascii=False) + "\n")
    return out


def export_json(records: Iterable[GenerationRecord], path: str | Path) -> Path:
    out = Path(path)
    out.parent.mkdir(parents=True, exist_ok=True)
    data = [record.to_dict() for record in records]
    out.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
    return out


def export_csv(records: Iterable[GenerationRecord], path: str | Path) -> Path:
    out = Path(path)
    out.parent.mkdir(parents=True, exist_ok=True)
    fields = [
        "request_id", "request_type", "user_prompt", "user_negative_prompt", "caption",
        "seed", "model_version", "model_uri", "width", "height", "aspect_ratio",
        "image_resolution", "style_expert", "creation_time_float", "private",
        "response_count", "response_ids", "sources",
    ]
    with out.open("w", encoding="utf-8", newline="") as fh:
        writer = csv.DictWriter(fh, fieldnames=fields)
        writer.writeheader()
        for record in records:
            writer.writerow({
                "request_id": record.request_id,
                "request_type": record.request_type,
                "user_prompt": record.user_prompt,
                "user_negative_prompt": record.user_negative_prompt,
                "caption": record.caption,
                "seed": record.seed,
                "model_version": record.model_version,
                "model_uri": record.model_uri,
                "width": record.width,
                "height": record.height,
                "aspect_ratio": record.aspect_ratio,
                "image_resolution": record.image_resolution,
                "style_expert": record.style_expert,
                "creation_time_float": record.creation_time_float,
                "private": record.private,
                "response_count": len(record.responses),
                "response_ids": "|".join(record.responses),
                "sources": "|".join(record.sources),
            })
    return out
