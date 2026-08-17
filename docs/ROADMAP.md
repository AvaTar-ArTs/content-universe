# Roadmap

## Phase 1 — Recovery Core
- [x] Canonical generation/response records
- [x] Asset / collection / profile records
- [x] Cross-media creative entities
- [x] Completeness-aware merge
- [x] Provenance ledger
- [x] Creative graph
- [x] SQLite persistence
- [x] JSON / JSONL / CSV exports
- [x] Browser userscript collector
- [x] Adapter registry
- [x] External adapter entry-point discovery
- [x] JSON Schema contracts
- [x] CI / lint / regression tests

## Phase 2 — Ideogram Intelligence
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
- [ ] Full response metadata batch enrichment workflow
- [ ] Resolution registry parser
- [ ] Color palette registry parser
- [ ] Reference collection resolver into canonical CollectionRecord entities
- [ ] Edit/remix lineage resolver across generations
- [ ] Generation-request payload fixture from a fresh generation capture
- [ ] Prompt Builder transformation fixture
- [ ] Character-reference request fixture
- [ ] Product-reference request fixture
- [ ] Style-reference request fixture
- [ ] Image Studio / Canvas evidence adapters

## Phase 3 — Suno Reunification
- [x] JSON export adapter
- [x] Flexible CSV adapter
- [x] Saved HTML adapter
- [x] Next.js `__NEXT_DATA__` recovery
- [x] Song-link ID fallback
- [ ] Import historical intelligent richer-row heuristics explicitly
- [ ] CSV dialect/schema profiler across historical exports
- [ ] Browser extractor bridge/export adapter
- [ ] Resume/session-state import
- [ ] Cover/audio asset manifests
- [ ] Lyrics/style normalized fields
- [ ] Publication/video relationships
- [ ] Existing master catalog migration command

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

## Phase 5 — Search & Intelligence
- [x] SQLite query layer
- [x] Basic prompt/content search
- [x] Model and request-type aggregation
- [x] Entity search
- [x] Lineage and provenance queries
- [ ] SQLite FTS5 index
- [ ] Embedding/vector index adapter
- [ ] Prompt component frequency analytics
- [ ] Style fingerprint clustering
- [ ] Prompt evolution / ancestry reports
- [ ] Duplicate / near-duplicate asset detection
- [ ] Cross-platform semantic reconciliation
- [ ] Dataset quality/completeness scoring reports

## Phase 6 — Interfaces
- [x] CLI
- [x] MCP server
- [x] Textual TUI
- [x] Ideogram userscript
- [ ] Browser extension
- [ ] Local HTTP service
- [ ] Local web dashboard
- [ ] TUI lineage explorer
- [ ] TUI asset gallery launcher
- [ ] MCP resources/templates in addition to tools
- [ ] Background local ingestion daemon

## Phase 7 — Creator OS Integration
- [ ] GitHub creative-repo adapter
- [ ] Google Drive / Library file adapter
- [ ] ComfyUI workflow/output adapter
- [ ] Leonardo adapter
- [ ] Generic image-generation manifest adapter
- [ ] Video-generation adapter
- [ ] Publication destinations / marketplace metadata
- [ ] Manga/comic/storyboard relationships
- [ ] Music/video/image campaign bundles
- [ ] Provenance-aware handoff dossier generator
- [ ] Creator asset dependency graph
- [ ] Release/publishing graph

## Research fixtures still worth capturing

The current architecture no longer depends on additional captures, but these would unlock deeper Ideogram-specific behavior:

1. fresh text-to-image generation from submit through completion
2. one edit/remix
3. one style-reference generation
4. one character-reference generation
5. one product-reference generation
6. one Prompt Builder transformation
7. one Canvas/Image Studio workflow

Raw captures remain local; only synthetic or reviewed sanitized fixtures should enter the repository.
