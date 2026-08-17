# Roadmap

This roadmap is maintained alongside [`CONVERSATION_SAVEPOINT_AUDIT.md`](CONVERSATION_SAVEPOINT_AUDIT.md). Checkboxes describe repository state, while the save-point audit explains where each requirement came from and whether it belongs to recovery, authoring, provider execution, or higher-order creator intelligence.

## Phase 1 — Recovery Core
- [x] Canonical generation/response records
- [x] Asset / collection / profile records
- [x] Cross-media creative entities
- [x] Completeness-aware merge
- [x] Provenance ledger
- [x] Creative graph
- [x] SQLite persistence
- [x] JSON / JSONL / CSV exports
- [x] Portable dataset packs with checksums
- [x] Browser userscript collector
- [x] Adapter registry
- [x] External adapter entry-point discovery
- [x] JSON Schema contracts
- [x] CI / lint / regression tests across Python 3.11, 3.12, and 3.13

## Phase 2 — Ideogram Recovery Intelligence
- [x] Offline HAR parser
- [x] Saved HTML recovery
- [x] Browser-export recovery
- [x] Cursor profile walker with caller-controlled transport
- [x] Model capability parser
- [x] Asset manifest parser
- [x] Public asset downloader boundary
- [x] Structured/autoprompt decomposition
- [x] HAR endpoint inventory
- [x] Conservative HAR sanitizer
- [x] Reference collection resolver into canonical `CollectionRecord` / `AssetRecord` entities
- [ ] Full response metadata batch enrichment workflow
- [ ] Resolution registry parser
- [ ] Color palette registry parser
- [ ] Cross-generation edit/remix lineage resolver
- [ ] Organization/workspace normalization
- [ ] Quota/cost/status observation models
- [ ] Canvas/document entities
- [ ] Generation-request payload fixture from a fresh generation capture
- [ ] Prompt Builder transformation fixture
- [ ] Character-reference request fixture
- [ ] Product-reference request fixture
- [ ] Style-reference request fixture
- [ ] Image Studio / Canvas evidence adapters
- [ ] Full `@avatararts` corpus ingestion and request/response/asset reconciliation
- [ ] Corpus-scale prompt/model/style evolution reports

## Phase 3 — Suno Reunification
- [x] JSON export adapter
- [x] Flexible CSV adapter
- [x] Saved HTML adapter
- [x] Next.js `__NEXT_DATA__` recovery
- [x] Song-link ID fallback
- [x] Shared completeness-aware richer-record merge
- [ ] Historical CSV dialect/schema profiler
- [ ] Suno browser extractor bridge/export adapter
- [ ] Resume/session-state import
- [ ] Cover/audio asset manifests
- [ ] Lyrics/style normalized fields
- [ ] Publication/video relationships
- [ ] Existing master catalog migration command
- [ ] Generic staged-enrichment queue with concurrency/retry/checkpoint state

## Phase 4 — Content Universe Graph
- [x] Projects / series / stories / characters
- [x] Chapters / scenes
- [x] Tracks / images / videos / prompts
- [x] Publications / products / campaigns / files
- [x] TOML / JSON creative-universe manifest
- [x] Explicit cross-media relationships
- [x] Manifest-to-SQLite persistence
- [x] Manifest-to-Mermaid export
- [ ] Link manifest entities directly to harvested request/response IDs from CLI
- [ ] Entity aliases / reconciliation assistant
- [ ] Series/project folder import
- [ ] Storyboard / comic layout entities
- [ ] Character bible and style bible schemas
- [ ] Timeline / chronology relationships

## Phase 5 — CreativeOS Contract Recovery

This phase restores the structured-authoring/runtime half that existed in the earlier iDeoMine/CreativeOS design but was not migrated into the first recovery-focused Content Universe implementation.

- [ ] Explicit product/layer contracts: Content Universe / CreativeOS / iDeoMine / Prompt Builder / Reference Genome / Asset Graph
- [ ] Provider-neutral semantic operation model
  - [ ] generate
  - [ ] edit
  - [ ] remix
  - [ ] reframe
  - [ ] upscale
  - [ ] remove background
  - [ ] describe
  - [ ] structured/layerized operations
- [ ] Semantic source-cardinality and no-silent-substitution validators
- [ ] `PromptManifest`
- [ ] `PromptLineage`
- [ ] typed `SceneGraph`
- [ ] typed `SceneElement` hierarchy
- [ ] `TypographyLayer`
- [ ] `StyleStack`
- [ ] portable `StyleDNA`
- [ ] `ReferenceGenome`
- [ ] creator canon / character identity anchors / approved reference sets
- [ ] evaluation and approval records
- [ ] original-prompt immutability tests
- [ ] authoring-reference vs generation-reference separation tests

## Phase 6 — Provider Runtime & Workflow Engine

Recovery adapters parse existing evidence. Provider backends perform live supported operations. Do not merge those contracts.

- [ ] `ProviderBackend` protocol
- [ ] `ProviderRegistry`
- [ ] provider capability registry
- [ ] provider dialect/translation layer
- [ ] mock backend for deterministic/credit-free tests
- [ ] remote MCP federation backend boundary
- [ ] policy-driven provider/model router
- [ ] workflow registry/engine
- [ ] asset-pack workflow
- [ ] character-system / manga-character-sheet workflow
- [ ] style-bible workflow
- [ ] storyboard workflow
- [ ] brand-campaign workflow
- [ ] manga/comic-page workflow
- [ ] product-mockup workflow
- [ ] custom-model training workflow
- [ ] explicit partial-failure model
- [ ] retries/backoff/rate-limit/cost/privacy state
- [ ] generation/job status events
- [ ] organizations/workspaces
- [ ] datasets and model-training records

## Phase 7 — Evaluation, Search & Creative Intelligence
- [x] SQLite query layer
- [x] Basic prompt/content search
- [x] Model and request-type aggregation
- [x] Entity search
- [x] Lineage and provenance queries
- [x] Optional SQLite FTS5 index helper
- [ ] Embedding/vector index adapter
- [ ] Prompt component frequency analytics
- [ ] Style fingerprint clustering
- [ ] Prompt evolution / ancestry reports
- [ ] Duplicate / near-duplicate asset detection
- [ ] Cross-platform semantic reconciliation
- [ ] Dataset quality/completeness scoring reports
- [ ] Character consistency evaluator
- [ ] Style consistency evaluator
- [ ] Text accuracy evaluator
- [ ] Layout compliance evaluator
- [ ] Story/visual continuity evaluator
- [ ] Human approval/rejection/revision gates
- [ ] Approved-output feedback into Reference Genome/training data

## Phase 8 — Durable Assets & Async Infrastructure
- [ ] Blob/object-store abstraction
- [ ] Content hashes and integrity verification
- [ ] Durable local/remote object locators
- [ ] MIME/size/dimension metadata
- [ ] Mirror/download policy
- [ ] Provider URL retained as provenance rather than durable identity
- [ ] Worker queue
- [ ] Webhook/event ingestion
- [ ] Background local ingestion daemon
- [ ] Idempotency/checkpoint model

## Phase 9 — Interfaces
- [x] Recovery/catalog CLI
- [x] Query-oriented MCP server
- [x] Query-oriented Textual TUI
- [x] Ideogram userscript
- [ ] CreativeOS semantic MCP tools
- [ ] Provider-control TUI views
- [ ] Browser extension / DevTools collector
- [ ] Local HTTP/REST service
- [ ] Local web studio/dashboard
- [ ] TUI lineage explorer
- [ ] TUI asset gallery launcher
- [ ] MCP resources/prompts/templates in addition to tools
- [ ] A2A agent server
- [ ] folder watcher

## Phase 10 — Creator Ecosystem Integration
- [ ] GitHub creative-repo adapter
- [ ] Google Drive / Library / local filesystem adapter
- [ ] ComfyUI workflow/output adapter
- [ ] Leonardo adapter
- [ ] FLUX / fal / Replicate adapters
- [ ] Generic image-generation manifest adapter
- [ ] Video-generation adapter
- [ ] Publication destinations / marketplace metadata
- [ ] Manga/comic/storyboard relationships
- [ ] Music/video/image campaign bundles
- [ ] Provenance-aware handoff dossier generator
- [ ] Creator asset dependency graph
- [ ] Release/publishing graph
- [ ] procedural Skills layer

## Research fixtures still worth capturing

The recovery architecture no longer depends on additional captures, but these would unlock deeper Ideogram-native behavior and contract tests:

1. fresh text-to-image generation from submit through completion
2. one edit
3. one remix/reframe/upscale example where available
4. one style-reference generation
5. one character-reference generation
6. one product-reference generation
7. one Prompt Builder transformation
8. one Canvas/Image Studio workflow

Raw captures remain local. Only synthetic or manually reviewed sanitized fixtures should enter the repository.
