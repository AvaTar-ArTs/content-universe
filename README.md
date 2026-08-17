# Content Universe

> A provenance-aware creative recovery, catalog, lineage, and intelligence layer for multimodal creator ecosystems.

Content Universe grew from the extraction/recovery patterns developed across the AvaTar-ArTs Suno tooling and the evidence captured from Ideogram. It generalizes those lessons into a platform-independent system that treats every creative artifact as an entity with identity, provenance, lineage, assets, prompts, references, and relationships.

Ideogram is the first deeply evidenced visual adapter family. Suno is the first cross-media recovery family. Above both is a project-level ontology for series, stories, characters, tracks, images, videos, publications, products, campaigns, and the other things that actually make a creator's work a universe instead of a download folder.

## The idea

Creator platforms scatter a project across prompts, generations, variants, edits, references, covers, audio, metadata, saved HTML, browser caches, public feeds, and exports. A normal scraper flattens those into rows and quietly loses the history that makes the work reusable.

Content Universe preserves the structure:

```text
Browser DOM ───────┐
HAR / network ─────┤
Saved HTML ────────┤
Exported JSON/CSV ─┼─> Platform Adapter
Public/API JSON ───┤         │
Suno archives ─────┘         ▼
                      Canonical entities
                 request / response / asset
                    collection / profile
                             │
                ┌────────────┼────────────┐
                ▼            ▼            ▼
             merge      provenance     lineage
                │            │            │
                └────────────┼────────────┘
                             ▼
                      Content Universe
                             │
          project / series / story / character
           chapter / scene / track / image / video
          publication / product / campaign / prompt
                             │
         ┌───────────────────┼───────────────────┐
         ▼                   ▼                   ▼
     JSON/JSONL             SQLite              Graph
         │                   │                   │
         └─────────────┬─────┴─────────────┬────┘
                       ▼                   ▼
                      MCP                 TUI
```

## v0.3 capabilities

### Recovery core

- canonical generation and response records
- asset, collection, profile, and typed entity references
- cross-media creative entities
- metadata completeness scoring
- provenance-preserving deep merge
- observation ledger with source, timestamp, locator, confidence, and metadata
- deduplicated creative graph
- conservative lineage extraction
- JSON, JSONL, and CSV exports
- SQLite persistence
- local query layer
- external adapter entry-point discovery

### Ideogram

- offline HAR ingestion
- recursive generation discovery inside captured JSON
- base64 HAR response decoding
- profile cursor-page discovery
- reusable cursor walker with caller-owned transport
- saved Ideogram HTML recovery
- userscript JSON export recovery
- stable `data-testid` identity extraction
- `/g/<generation>/<index>` parsing
- `/response/<response-id>@<resolution>` asset parsing
- response/asset manifest generation
- public asset downloader with explicit host allowlist and no browser credentials
- model capability extraction/filtering
- structured/autoprompt composition decomposition
- network endpoint inventory from HAR without request replay
- conservative HAR sanitizer for fixture preparation
- browser field collector with adaptive scrolling, resume, lazy-load nudges, copy/export

### Suno

- JSON export normalization
- flexible CSV recovery with ID discovery across historical column shapes
- saved HTML recovery
- `__NEXT_DATA__` structured-state recovery
- link fallback when metadata shapes change
- audio URL, cover metadata, lyrics, tags, prompt, title, and raw source preservation
- shared richer-record merge rather than another isolated Suno database

### Content-universe manifests

A TOML or JSON manifest can declare your own higher-order creative structure:

```toml
[universe]
name = "My Universe"

[[entities]]
id = "series-a"
kind = "series"
title = "Series A"

[[entities]]
id = "hero-a"
kind = "character"
title = "Hero A"

[[relationships]]
source = "series:series-a"
kind = "features"
target = "character:hero-a"
```

That means harvested platform artifacts and explicit creative intent can live in the same graph.

### Interfaces

- zero-dependency core CLI
- optional MCP server
- optional Textual TUI
- browser userscript field collector
- Python adapter SDK / entry points

## Install

```bash
git clone https://github.com/AvaTar-ArTs/content-universe.git
cd content-universe
python -m pip install -e .
```

Development:

```bash
python -m pip install -e '.[dev]'
```

MCP:

```bash
python -m pip install -e '.[mcp]'
```

TUI:

```bash
python -m pip install -e '.[tui]'
```

## Quick starts

### Recover an Ideogram HAR

```bash
content-universe harvest ~/Downloads/ideogram.ai-avatararts.har \
  --summary \
  --sqlite catalogs/avatararts.sqlite \
  --jsonl catalogs/avatararts.jsonl \
  --csv catalogs/avatararts.csv \
  --asset-manifest catalogs/avatararts.assets.json \
  --mermaid catalogs/avatararts.mmd
```

### Recover saved Ideogram HTML

```bash
content-universe harvest saved-ideogram-profile.html --jsonl recovered.jsonl
```

### Import a browser userscript export

```bash
content-universe harvest content-universe-ideogram-2026-08-17.json --sqlite catalogs/avatararts.sqlite
```

### Recover a Suno CSV

```bash
content-universe harvest suno-master.csv --sqlite catalogs/music.sqlite --summary
```

### Recover saved Suno HTML

```bash
content-universe harvest saved-suno-library.html --jsonl catalogs/recovered-suno.jsonl
```

### Inventory an Ideogram HAR

```bash
content-universe network-inventory ideogram.ai-all.har --host ideogram.ai
```

This analyzes captured traffic only. It does not replay requests.

### Analyze an Ideogram autoprompt

```bash
content-universe prompt-analyze \
  --original 'make a poster' \
  --expanded @expanded-prompt.json
```

### Inspect captured model capabilities

```bash
content-universe models-from-json model-catalog.json \
  --capability supports_character_reference
```

### Create a cross-media universe manifest

```bash
content-universe manifest-template --output my-universe.toml
```

Load and persist it:

```bash
content-universe manifest-load my-universe.toml \
  --summary \
  --sqlite catalogs/universe.sqlite \
  --mermaid catalogs/universe.mmd
```

## TUI

```bash
content-universe-tui --db catalogs/avatararts.sqlite
```

The local TUI provides prompt search and record inspection without requiring a hosted service.

## MCP

```bash
content-universe-mcp --db catalogs/avatararts.sqlite
```

MCP tools cover:

```text
catalog_stats
get_generation
get_response
get_asset
get_collection
get_profile
get_creative_entity
search_prompts
search_entities
entity_kind_counts
model_counts
request_type_counts
lineage
provenance
assets_for_response
```

The MCP server queries the durable catalog. It does not own browser credentials or scrape third-party sites.

## Browser harvester

Install:

```text
browser/ideogram-harvester.user.js
```

The userscript carries the mature Suno extractor pattern forward:

```text
semantic ID accumulator
MutationObserver discovery
adaptive scroll-container selection
lazy-load triggering
reverse nudge
idle-cycle stop
sessionStorage resume
copy/export
```

It deliberately does **not** monkey-patch Ideogram's `fetch`, replay authenticated requests, or export session material.

## Structured prompt intelligence

Some captured Ideogram response prompts are structured composition specifications rather than plain text. `promptlab.py` preserves and decomposes shapes such as:

```text
high_level_description
compositional_deconstruction
  background
  elements[]
    type
    text
    desc
```

This keeps the creator's original prompt distinct from Ideogram's expanded/autoprompt and makes typography/object/background structure searchable later.

## External adapters

Third-party packages can register adapters with Python entry points:

```toml
[project.entry-points."content_universe.adapters"]
myplatform = "my_package:MyAdapter"
```

The core stays platform-independent while Leonardo, ComfyUI, local workflows, Drive exports, or future services can plug into the same `HarvestResult` contract.

## Security

**Never commit raw authenticated HAR files.**

HAR captures can contain cookies, bearer tokens, Cloudflare clearance data, account identifiers, request headers, and private URLs.

The repository ignores common sensitive/local artifacts, but `.gitignore` is not a security boundary. `content-universe sanitize-har` produces only a candidate redacted copy. Manually review every fixture before publication.

See [`SECURITY.md`](SECURITY.md).

## Repository map

```text
src/content_universe/
├── adapters/
│   ├── base.py
│   ├── ideogram/
│   │   ├── assets.py
│   │   ├── browser_export.py
│   │   ├── har.py
│   │   ├── html.py
│   │   ├── models.py
│   │   └── profile.py
│   └── suno/
│       ├── csv.py
│       ├── export.py
│       └── html.py
├── catalog.py
├── cli.py
├── exporters.py
├── graph.py
├── ideogram.py
├── lineage.py
├── manifest.py
├── mcp_server.py
├── models.py
├── network.py
├── plugins.py
├── promptlab.py
├── provenance.py
├── query.py
├── sanitize.py
├── storage.py
├── tui.py
└── universe.py

browser/
fixtures/
schemas/
docs/
examples/
tests/
```

## Documentation

- [`docs/ARCHITECTURE.md`](docs/ARCHITECTURE.md)
- [`docs/DATA_MODEL.md`](docs/DATA_MODEL.md)
- [`docs/ADAPTER_SPEC.md`](docs/ADAPTER_SPEC.md)
- [`docs/IDEOGRAM_EVIDENCE.md`](docs/IDEOGRAM_EVIDENCE.md)
- [`docs/SUNO_HERITAGE.md`](docs/SUNO_HERITAGE.md)
- [`docs/CLI.md`](docs/CLI.md)
- [`docs/MCP.md`](docs/MCP.md)
- [`docs/ROADMAP.md`](docs/ROADMAP.md)

## Design rules

1. Structured sources beat brittle CSS scraping.
2. Identity is resolved before data is flattened.
3. Discovery and deep enrichment are separate phases.
4. Richer records augment earlier records without erasing provenance.
5. Request, response, asset, collection, and project identities stay distinct.
6. Raw captures stay local; public fixtures are synthetic/sanitized derivatives.
7. Platform-specific logic belongs in adapters.
8. Browser collectors are field tools, not databases.
9. Relationships are emitted only when evidence supports them.
10. The final product is a graph of creative work, not a folder of downloads.

## License

MIT.
