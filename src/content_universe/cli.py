from __future__ import annotations

import argparse
import json
from pathlib import Path

from .ideogram import catalog_from_har, profile_pages_from_har


def _write_jsonl(path: str | Path, records: list[dict]) -> None:
    output = Path(path)
    with output.open("w", encoding="utf-8") as handle:
        for record in records:
            handle.write(json.dumps(record, ensure_ascii=False) + "\n")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="content-universe")
    sub = parser.add_subparsers(dest="command", required=True)

    ideogram = sub.add_parser("ideogram-har", help="Parse an Ideogram HAR offline")
    ideogram.add_argument("har", help="Path to HAR capture")
    ideogram.add_argument("--summary", action="store_true", help="Print catalog summary")
    ideogram.add_argument("--jsonl", help="Export normalized generation records as JSONL")
    ideogram.add_argument("--show-profile-pages", action="store_true", help="Report captured profile cursor pages")
    return parser


def main() -> int:
    args = build_parser().parse_args()

    if args.command == "ideogram-har":
        catalog = catalog_from_har(args.har)
        if args.summary or not args.jsonl:
            print(json.dumps(catalog.summary(), indent=2))

        if args.show_profile_pages:
            pages = profile_pages_from_har(args.har)
            print(json.dumps({"captured_profile_pages": len(pages)}, indent=2))

        if args.jsonl:
            records = [record.to_dict() for record in catalog.generations.values()]
            _write_jsonl(args.jsonl, records)
            print(f"wrote {len(records)} normalized generations to {args.jsonl}")

        return 0

    return 1


if __name__ == "__main__":
    raise SystemExit(main())
