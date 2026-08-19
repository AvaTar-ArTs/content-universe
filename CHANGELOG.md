# Changelog

All notable project changes are recorded here. The project is still pre-1.0; architecture and contracts may evolve, but semantic/provenance invariants should remain stable unless explicitly revised.

## Unreleased

### Polyglot CreativeOS foundation

- Added shared JSON Schemas for provider-neutral prompt manifests and workflow graphs.
- Added TypeScript contract helpers, Prompt Builder browser starter, Rust indexer, Go gateway, Swift CreativeOSKit, PostgreSQL substrate, declarative workflow, and polyglot CI.


### Conversation and migration audit

- Added `docs/CONVERSATION_SAVEPOINT_AUDIT.md`, reconstructing the Ideogram/Suno/iDeoMine/CreativeOS evolution as chronological save points and comparing each checkpoint against the repository.
- Added `docs/CREATIVEOS_MIGRATION_AUDIT.md`, comparing archived CreativeOS/iDeoMine behavior against recovery-focused Content Universe and the merged architecture.
- Recovered the designed distinction between Content Universe, CreativeOS, iDeoMine, Prompt Builder, Reference Genome, Skills, and Asset Graph.
- Reworked `docs/ARCHITECTURE.md` to model both recovery/evidence and creative-authoring directions.
- Reworked `docs/ROADMAP.md` to separate recovery adapters, provider dialects, provider backends, workflows, evaluation, and durable infrastructure.
- Corrected roadmap drift for already-implemented Ideogram reference collection normalization and optional FTS5 support.

### CreativeOS contract recovery

- Added `content_universe.creativeos` as a typed provider-neutral authoring/runtime contract layer above the existing durable Content Universe graph.
- Added semantic operation contracts for generate, edit, remix, reframe, upscale, background removal, describe, Magic Prompt, and Layerize Text.
- Added source-cardinality validation and executable no-silent-substitution invariants.
- Added explicit authoring, generation, evaluation, and continuity reference roles. `passed_to_generation` is derived from role to prevent contradictory state.
- Added immutable `PromptLineage` and `PromptManifest`, preserving the creator's original prompt across enhancements, localization, reflow, provider dialects, and provider-expanded prompts.
- Added typed `SceneGraph`, scene elements, bounding boxes, `TypographyLayer`, reusable entity/concept identity linkage, and `INSTANCE_OF` graph persistence.
- Added `StyleStack` and portable `StyleDNA` rather than reducing simultaneous style mechanisms to one scalar field.
- Added `ReferenceGenome` and approved reference-entry contracts.
- Added `EvaluationRecord` and `ApprovalRecord` with durable Content Universe graph integration.
- Added `ProviderBackend`, `ProviderRegistry`, `ProviderCapabilities`, and `ProviderDialect` contracts, deliberately separate from recovery adapters.
- Added `DeterministicMockBackend`, using semantic-request hashes for reproducible job/output IDs and explicitly reporting mock rather than provider execution.
- Added a local `PromptBuilder` runtime for build/import/deconstruct/compose/reference/enhance/validate/localize/reflow/export.
- Provider-backed Prompt Builder methods now emit an explicit `ProviderOperationRequired` boundary rather than simulating Describe, Magic Prompt, Layerize Text, or provider-backed edit results.
- Added an observed-field `IdeogramJsonDialect` that imports/exports the structured prompt shape established by captured Ideogram evidence while preserving unknown provider fields.
- Added a separate `providers` execution namespace and declarative Ideogram/iDeoMine catalog preserving the historical 26-tool surface without reintroducing string-based workflow coupling.
- Added reusable `concept` entities for repeated slogans/symbols/motifs and scene-instance links to canonical Character/Concept identities.
- Added `StructuredDesignAsset`, `Mask`, and `GenerationWindow` contracts so editable creative objects can bind base assets, SceneGraphs, PromptManifests, StyleDNA, vectors, targeted edit regions, and parent design lineage.
- Added persistence bridges so Prompt Manifests, SceneGraphs, StyleDNA, Reference Genomes, StructuredDesignAssets, evaluations, and approvals reuse the existing Content Universe entity/graph substrate instead of creating a second state store.

### Graph identity and persistence

- Fixed a continuity/data-loss bug discovered by the new entity-instance tests: two appearances of the same canonical character in one SceneGraph previously collapsed because graph identity was only `(source, target, kind)`.
- Added optional `GraphEdge.edge_id`; ordinary relationships retain historical deduplication while instance-sensitive relationships can use a stable per-edge identity such as a `SceneElement.element_id`.
- Scene `INSTANCE_OF` edges now use their element IDs so repeated appearances of the same character/concept remain distinct.
- Migrated SQLite `graph_edges` identity from `(source, target, kind)` to `(source, target, kind, edge_id)`.
- Added an automatic in-place migration for existing catalogs, preserving legacy edges as `edge_id=''` rather than requiring a fresh database.
- Updated graph JSON Schema and lineage queries to expose edge identity while remaining compatible with unmigrated read-only catalogs.

### Tests

- Added semantic operation/source-cardinality tests.
- Added original-prompt immutability and reference-role tests.
- Added deterministic mock-provider tests.
- Added structured Ideogram JSON round-trip and Prompt Builder boundary tests.
- Added CreativeOS-to-Content-Universe persistence tests.
- Added scene instance-to-entity graph tests.
- Added the historical 26-tool Ideogram provider catalog parity test.
- Added StructuredDesignAsset dependency/derivative graph tests.
- Added multi-instance graph storage and legacy SQLite migration regression tests.
- Verified the resulting head across Python 3.11, 3.12, and 3.13 with install, Ruff, pytest, and compile all succeeding.

### Next architectural checkpoint

The next high-value work is no longer contract reconstruction. It is runtime orchestration and durability:

- decide sync/async policy for real provider backends,
- build Workflow Engine v2 over typed semantic operations and provider-state services,
- restore asset-pack / character-system / style-training workflows without the old stringly provider coupling,
- add continuity constraints and targeted regeneration plans,
- add durable blob/object storage with hashes and integrity checks,
- pressure-test the system against the accessible full Ideogram archive.

Live provider execution should only be layered on through supported provider transports and must preserve the restored semantic invariants.

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
