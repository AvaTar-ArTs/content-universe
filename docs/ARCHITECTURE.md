# Architecture

Content Universe is a multimodal recovery and provenance system, not a scraper collection.

## System layers

```text
┌──────────────────────────────────────────────────────────────┐
│  Acquisition                                                 │
│  HAR · saved HTML · JSON/CSV · userscript · API transport   │
└──────────────────────────────┬───────────────────────────────┘
                               ▼
┌──────────────────────────────────────────────────────────────┐
│  Platform adapters                                            │
│  Ideogram · Suno · external entry-point plugins              │
└──────────────────────────────┬───────────────────────────────┘
                               ▼
┌──────────────────────────────────────────────────────────────┐
│  Canonical platform entities                                  │
│  generation · response · asset · collection · profile        │
└──────────────────────────────┬───────────────────────────────┘
                               ▼
┌──────────────────────────────────────────────────────────────┐
│  Recovery intelligence                                        │
│  completeness merge · provenance · conservative lineage      │
└──────────────────────────────┬───────────────────────────────┘
                               ▼
┌──────────────────────────────────────────────────────────────┐
│  Creative universe entities                                   │
│  project · series · story · character · chapter · scene      │
│  track · image · video · prompt · publication · product      │
│  campaign · file                                              │
└──────────────────────────────┬───────────────────────────────┘
                               ▼
┌──────────────────────────────────────────────────────────────┐
│  Persistence & graph                                          │
│  SQLite · JSON/JSONL/CSV · Mermaid · asset manifests         │
└──────────────────────────────┬───────────────────────────────┘
                               ▼
┌──────────────────────────────────────────────────────────────┐
│  Interfaces                                                   │
│  CLI · MCP · TUI · browser collector · future dashboard      │
└──────────────────────────────────────────────────────────────┘
```

## Core rule: identity before interpretation

A generation request, its responses, and its media assets are different objects.

```text
Generation / Request
  ├─ Response 0
  │    ├─ preview asset
  │    └─ original asset
  ├─ Response 1
  └─ Reference Collections
```

Flattening those prematurely makes later edit/remix/reference lineage ambiguous.

## Two graphs, one system

Content Universe uses one generic `CreativeGraph`, but conceptually it contains two kinds of relationships.

### Platform provenance/lineage

```text
generation --produced--> response
request --style_reference--> collection
request --edit_of--> source asset
```

### Creator-intent relationships

```text
series --features--> character
track --soundtrack_for--> series
image --cover_for--> story
publication --adapts--> story
prompt --prompt_for--> image
```

The same graph lets an explicitly authored creative entity connect to harvested platform IDs.

## ContentUniverse aggregate

`ContentUniverse` groups:

```text
Catalog              generations + responses
assets               AssetRecord map
collections          CollectionRecord map
profiles             ProfileRecord map
entities              CreativeEntity map
graph                 CreativeGraph
provenance            ProvenanceLedger
metadata              universe/run metadata
warnings              non-fatal recovery warnings
```

This is the main in-memory composition root.

## Adapter architecture

`Adapter` is intentionally small:

```python
supports(source) -> bool
harvest(source) -> HarvestResult
```

`HarvestResult` carries:

```text
GenerationRecord[]
CreativeGraph
ProvenanceLedger
metadata
warnings
```

Adapters do not own persistence, MCP, or browser credentials.

## Ideogram adapter family

```text
ideogram/
├── har.py              offline captured JSON recovery
├── html.py             saved semantic DOM recovery
├── browser_export.py   userscript observation import
├── profile.py          cursor URL + transport-independent walker
├── models.py           model capability extraction
└── assets.py           asset parsing/manifests/public downloader
```

The legacy-compatible `content_universe.ideogram` module contains the low-level generation/HAR normalization functions used by the adapter family.

## Suno adapter family

```text
suno/
├── export.py           JSON exports
├── csv.py              flexible historical CSV recovery
└── html.py             saved HTML + __NEXT_DATA__ + link fallback
```

This is where the older Suno extractor/recovery ecosystem gets progressively migrated into the shared architecture.

## Merge semantics

The canonical `Catalog` applies completeness-aware merging.

A later source may be richer, but it does not erase earlier source history.

```text
sparse DOM record
      +
profile API record
      +
response enrichment
      ↓
canonical record + combined provenance
```

## Provenance

Provenance is intentionally separate from raw payloads.

An observation contains:

```text
source
observed_at
locator
confidence
metadata
```

This allows the system to distinguish "the current canonical value" from "all the places this fact came from."

## Persistence

SQLite stores both indexed columns and full JSON payloads.

Tables:

```text
generations
responses
assets
collections
profiles
creative_entities
graph_edges
provenance
universe_metadata
```

This gives the project an evolvable schema without throwing away new platform fields.

## MCP boundary

MCP queries SQLite. It does not browse creator platforms.

That keeps:

- authentication outside the agent server
- tests deterministic
- live platform changes isolated to adapters
- the same catalog usable by CLI/TUI/scripts

## Browser boundary

The userscript is an observational field collector. It intentionally avoids hooking the platform's authentication/network stack.

It borrows mature Suno ideas:

- canonical ID map
- adaptive scrolling
- lazy-load nudging
- idle-stop
- session resume
- passive mutation observation
- export

but sends the result through the same adapter/core contracts.

## External plugins

Python entry points under:

```text
content_universe.adapters
```

can register new platform adapters without editing the core package.

## Security boundary

Raw authenticated captures are private local evidence.

Public repository inputs should be:

- synthetic fixtures
- manually reviewed sanitized fixtures
- normalized records
- endpoint/schema summaries with secrets/query values removed

No raw browser cookies, bearer tokens, or private HARs belong in source control.
