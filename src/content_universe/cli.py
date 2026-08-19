from __future__ import annotations

import argparse
import json
from pathlib import Path

from .adapters import default_registry
from .adapters.ideogram.assets import manifest_from_records, write_manifest
from .adapters.ideogram.models import filter_models, model_records
from .audit import audit_records
from .bulk import analyze_discovery, discover_folder_sources
from .dataset_pack import build_dataset_pack
from .exporters import export_csv, export_json, export_jsonl
from .fts import rebuild_fts
from .manifest import manifest_template, universe_from_manifest
from .network import endpoint_summary
from .pipeline import harvest_sources, merge_universes
from .promptlab import decompose_prompt, prompt_fingerprint
from .sanitize import sanitize_har
from .storage import SQLiteStore
from .universe import ContentUniverse


def _add_universe_outputs(parser: argparse.ArgumentParser) -> None:
    parser.add_argument("--json", help="generation array JSON")
    parser.add_argument("--jsonl", help="generation JSONL")
    parser.add_argument("--csv", help="generation CSV")
    parser.add_argument("--universe-json", help="full universe JSON including graph/provenance/entities")
    parser.add_argument("--sqlite")
    parser.add_argument("--mermaid")
    parser.add_argument("--asset-manifest")
    parser.add_argument("--pack", help="portable normalized dataset ZIP")
    parser.add_argument("--summary", action="store_true")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="content-universe", description="Recover, normalize, inspect and graph creative platform data.")
    sub = parser.add_subparsers(dest="command", required=True)

    harvest = sub.add_parser("harvest", help="Auto-detect one supported source and normalize it")
    harvest.add_argument("source")
    _add_universe_outputs(harvest)

    batch = sub.add_parser("batch", help="Harvest many sources into one merged Content Universe")
    batch.add_argument("sources", nargs="+")
    batch.add_argument("--manifest", action="append", default=[], help="merge a TOML/JSON creative-universe manifest")
    batch.add_argument("--ignore-unsupported", action="store_true")
    _add_universe_outputs(batch)

    folder = sub.add_parser("analyze-folder", help="Discover and analyze every supported source in a folder")
    folder.add_argument("folder")
    folder.add_argument("--no-recursive", action="store_true", help="only inspect direct children of the folder")
    folder.add_argument("--include", action="append", default=[], help="glob pattern to include; may be repeated")
    folder.add_argument("--exclude", action="append", default=[], help="glob pattern to exclude; may be repeated")
    folder.add_argument("--max-files", type=int, help="maximum number of candidate files to inspect")
    folder.add_argument("--strict", action="store_true", help="fail on unsupported files or per-file analysis errors")
    folder.add_argument("--discovery-json", help="write supported/unsupported/skipped discovery details as JSON")
    folder.add_argument("--analysis-json", help="write discovery, failures, and universe summary as JSON")
    _add_universe_outputs(folder)

    sub.add_parser("adapters", help="List registered adapters")

    audit = sub.add_parser("audit", help="Audit completeness across one or more sources")
    audit.add_argument("sources", nargs="+")
    audit.add_argument("--ignore-unsupported", action="store_true")
    audit.add_argument("--json")

    index = sub.add_parser("index", help="Build/rebuild optional SQLite FTS5 search indexes")
    index.add_argument("sqlite")

    network = sub.add_parser("network-inventory", help="Inventory endpoints from a HAR without replaying requests")
    network.add_argument("har")
    network.add_argument("--host")
    network.add_argument("--json")

    sanitize = sub.add_parser("sanitize-har", help="Create a conservatively redacted HAR copy for manual review")
    sanitize.add_argument("input")
    sanitize.add_argument("output")
    sanitize.add_argument("--strip-response-bodies", action="store_true")

    prompt = sub.add_parser("prompt-analyze", help="Analyze an original + expanded/autoprompt pair")
    prompt.add_argument("--original")
    prompt.add_argument("--expanded", required=True, help="Prompt string, structured JSON string, or @file.json")

    models = sub.add_parser("models-from-json", help="Extract Ideogram model capability records from captured JSON")
    models.add_argument("json_file")
    models.add_argument("--capability")
    models.add_argument("--custom", choices=["yes", "no"])

    manifest_init = sub.add_parser("manifest-template", help="Print or write a starter cross-media universe manifest")
    manifest_init.add_argument("--output")

    manifest_load = sub.add_parser("manifest-load", help="Load a .toml/.json universe manifest")
    manifest_load.add_argument("manifest")
    manifest_load.add_argument("--sqlite")
    manifest_load.add_argument("--mermaid")
    manifest_load.add_argument("--universe-json")
    manifest_load.add_argument("--pack")
    manifest_load.add_argument("--summary", action="store_true")
    return parser


def _load_arg(value: str):
    if value.startswith("@"):
        return Path(value[1:]).read_text(encoding="utf-8")
    return value


def _emit_universe(universe: ContentUniverse, args: argparse.Namespace) -> None:
    records = list(universe.generations.values())
    requested_output = any(
        getattr(args, name, None)
        for name in ("json", "jsonl", "csv", "universe_json", "sqlite", "mermaid", "asset_manifest", "pack")
    )
    if getattr(args, "summary", False) or not requested_output:
        print(json.dumps(universe.summary(), indent=2, ensure_ascii=False))
    if getattr(args, "json", None):
        export_json(records, args.json)
    if getattr(args, "jsonl", None):
        export_jsonl(records, args.jsonl)
    if getattr(args, "csv", None):
        export_csv(records, args.csv)
    if getattr(args, "universe_json", None):
        Path(args.universe_json).write_text(json.dumps(universe.to_dict(), indent=2, ensure_ascii=False), encoding="utf-8")
    if getattr(args, "asset_manifest", None):
        write_manifest(manifest_from_records(records), args.asset_manifest)
    if getattr(args, "pack", None):
        pack_path = build_dataset_pack(universe, args.pack)
        print(f"wrote dataset pack {pack_path}")
    if getattr(args, "sqlite", None):
        with SQLiteStore(args.sqlite) as store:
            store.save_universe(universe)
            print(json.dumps({"sqlite": str(args.sqlite), **store.stats()}, indent=2))
    if getattr(args, "mermaid", None):
        Path(args.mermaid).write_text(universe.graph.to_mermaid(), encoding="utf-8")


def main() -> int:
    args = build_parser().parse_args()
    registry = default_registry()

    if args.command == "adapters":
        for adapter in registry.adapters:
            print(adapter.name)
        return 0

    if args.command == "harvest":
        universe = harvest_sources([args.source], registry=registry)
        _emit_universe(universe, args)
        return 0

    if args.command == "batch":
        universe = harvest_sources(args.sources, registry=registry, ignore_unsupported=args.ignore_unsupported)
        for manifest_path in args.manifest:
            merge_universes(universe, universe_from_manifest(manifest_path))
        _emit_universe(universe, args)
        return 0

    if args.command == "analyze-folder":
        discovery = discover_folder_sources(
            args.folder,
            registry=registry,
            recursive=not args.no_recursive,
            include=args.include,
            exclude=args.exclude,
            max_files=args.max_files,
        )
        if args.discovery_json:
            Path(args.discovery_json).write_text(
                json.dumps(discovery.to_dict(), indent=2, ensure_ascii=False),
                encoding="utf-8",
            )
        analysis = analyze_discovery(discovery, registry=registry, continue_on_error=not args.strict)
        if args.analysis_json:
            Path(args.analysis_json).write_text(
                json.dumps(analysis.to_dict(), indent=2, ensure_ascii=False),
                encoding="utf-8",
            )
        if args.strict and discovery.unsupported:
            print(json.dumps(analysis.to_dict(), indent=2, ensure_ascii=False))
            return 2
        _emit_universe(analysis.universe, args)
        return 0

    if args.command == "audit":
        universe = harvest_sources(args.sources, registry=registry, ignore_unsupported=args.ignore_unsupported)
        report = audit_records(universe.generations.values()).to_dict()
        report["universe"] = universe.summary()
        text = json.dumps(report, indent=2, ensure_ascii=False)
        if args.json:
            Path(args.json).write_text(text, encoding="utf-8")
        else:
            print(text)
        return 0

    if args.command == "index":
        print(json.dumps(rebuild_fts(args.sqlite), indent=2))
        return 0

    if args.command == "network-inventory":
        data = endpoint_summary(args.har, host=args.host)
        text = json.dumps(data, indent=2, ensure_ascii=False)
        if args.json:
            Path(args.json).write_text(text, encoding="utf-8")
        else:
            print(text)
        return 0

    if args.command == "sanitize-har":
        payload = json.loads(Path(args.input).read_text(encoding="utf-8"))
        sanitized = sanitize_har(payload, strip_response_bodies=args.strip_response_bodies)
        Path(args.output).write_text(json.dumps(sanitized, indent=2, ensure_ascii=False), encoding="utf-8")
        print(f"wrote sanitized HAR candidate to {args.output}; manually review before publishing")
        return 0

    if args.command == "prompt-analyze":
        expanded = _load_arg(args.expanded)
        analysis = decompose_prompt(args.original, expanded)
        print(json.dumps({"decomposition": analysis.to_dict(), "fingerprint": prompt_fingerprint(analysis)}, indent=2, ensure_ascii=False))
        return 0

    if args.command == "models-from-json":
        payload = json.loads(Path(args.json_file).read_text(encoding="utf-8"))
        records = model_records(payload)
        custom = None if args.custom is None else args.custom == "yes"
        records = filter_models(records, capability=args.capability, custom=custom)
        print(json.dumps([record.to_dict() for record in records], indent=2, ensure_ascii=False))
        return 0

    if args.command == "manifest-template":
        template = manifest_template()
        if args.output:
            Path(args.output).write_text(template, encoding="utf-8")
            print(f"wrote {args.output}")
        else:
            print(template, end="")
        return 0

    if args.command == "manifest-load":
        universe = universe_from_manifest(args.manifest)
        if args.universe_json:
            Path(args.universe_json).write_text(json.dumps(universe.to_dict(), indent=2, ensure_ascii=False), encoding="utf-8")
        if args.pack:
            print(f"wrote dataset pack {build_dataset_pack(universe, args.pack)}")
        if args.sqlite:
            with SQLiteStore(args.sqlite) as store:
                store.save_universe(universe)
                print(json.dumps({"sqlite": str(args.sqlite), **store.stats()}, indent=2))
        if args.mermaid:
            Path(args.mermaid).write_text(universe.graph.to_mermaid(), encoding="utf-8")
        if args.summary or not (args.sqlite or args.mermaid or args.universe_json or args.pack):
            print(json.dumps(universe.summary(), indent=2, ensure_ascii=False))
        return 0

    return 1


if __name__ == "__main__":
    raise SystemExit(main())
