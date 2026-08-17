# Changelog

All notable project changes are recorded here. The project is still pre-1.0; architecture and contracts may evolve, but semantic/provenance invariants should remain stable unless explicitly revised.

## Unreleased

### Conversation parity audit

- Added `docs/CONVERSATION_SAVEPOINT_AUDIT.md`, reconstructing the Ideogram/Suno/iDeoMine/CreativeOS evolution as chronological save points and comparing each checkpoint against the repository.
- Recovered the previously designed distinction between Content Universe, CreativeOS, iDeoMine, Prompt Builder, Reference Genome, Skills, and Asset Graph.
- Identified the central migration gap: recovery/catalog/graph functionality was substantially implemented, while structured authoring, provider execution semantics, workflow orchestration, evaluation, and reusable creative memory were mostly not migrated.
- Reworked `docs/ARCHITECTURE.md` to model both recovery/evidence and creative-authoring directions.
- Reworked `docs/ROADMAP.md` to separate recovery adapters from provider backends and to add explicit CreativeOS contract/runtime phases.
- Corrected roadmap drift for already-implemented Ideogram reference collection normalization and optional FTS5 support.

### Next architectural checkpoint

Provider-neutral contracts should be restored before live provider transports:

- semantic operation contracts and no-silent-substitution validators,
- `PromptManifest` and `PromptLineage`,
- `SceneGraph` and `TypographyLayer`,
- `StyleStack` / `StyleDNA`,
- `ReferenceGenome`,
- provider capability/backend/dialect protocols,
- evaluation/approval records.

Live provider execution should only be layered on after those semantics are stable and tested.

## 0.3.0 — 2026-08-17

### Added

- Content Universe aggregate and cross-media creative entity model.
- Provenance ledger and creative graph.
- SQLite persistence, query layer, JSON/JSONL/CSV exporters, and optional FTS5 helper.
- Ideogram recovery adapters for HAR, saved HTML, browser exports, profile cursor traversal, model capabilities, assets, and references.
- Suno recovery adapters for JSON, flexible CSV, saved HTML, and `__NEXT_DATA__` state.
- Adaptive Ideogram userscript derived from mature Suno collector patterns.
- CLI, query-oriented MCP server, Textual TUI, adapter plugin entry points, schemas, synthetic fixtures, security documentation, Docker support, and CI.
- Network inventory and HAR sanitization helpers.
- Portable dataset packs with manifests/checksums.
- Research and engineering handoff documentation.

### Fixed

- Saved Ideogram HTML parsing now preserves `/g/<generation>/<response-index>` context across separately encountered lazy-loaded image tags.

### Verification

CI passed installation, Ruff, pytest, and Python compilation on Python 3.11, 3.12, and 3.13 after the HTML-context fix.

## 0.1.0 — 2026-08-17

- Initial empty-repository scaffold.
- Canonical generation/response records and completeness-aware merge.
- Offline Ideogram HAR normalization.
- Minimal CLI and regression tests.
- Security exclusions for raw authenticated HAR/session material.
