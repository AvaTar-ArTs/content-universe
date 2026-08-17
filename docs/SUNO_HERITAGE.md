# Suno Heritage

Content Universe is not replacing the historical AvaTar-ArTs Suno extractor work. It is extracting the strongest architectural ideas from that work and making them reusable across creative platforms.

## The Suno extractor family

The historical system evolved through multiple browser extractors, offline HTML parsers, merge tools, comparison scripts, shared utilities, automation dashboards, and cover-art download helpers.

Representative capability families included:

```text
live page accumulation
auto-scroll / lazy-load triggering
song UUID deduplication
detail-page enrichment
lyrics and summary recovery
retry / concurrency controls
session resume / partial recovery
CSV / JSON / Sheets export
saved HTML parsing
Next.js embedded-state parsing
multi-source merge
richer-row preference
cover asset downloading
catalog comparison
```

The strength was not any single userscript. It was the redundancy of recovery paths around one canonical catalog.

## What Content Universe inherits

### Canonical ID accumulator

Suno:

```text
Map<songUUID, Song>
```

Content Universe:

```text
request_id -> generation
response_id -> response
asset_id -> asset
collection_id -> collection
```

The multi-index model is necessary because image-generation requests commonly produce multiple responses and those responses may later become reference parents.

### Staged enrichment

Suno first discovered lightweight song records, then fetched details such as lyrics and tags.

Content Universe formalizes that as:

```text
discover -> normalize -> enrich -> merge -> graph -> persist
```

### Intelligent merge

The historical merge system recognized Suno IDs across fragmented CSVs and preferred richer rows.

Content Universe generalizes that principle:

- canonical identity never changes
- missing fields are filled
- structured dictionaries deep-merge
- list identifiers union
- raw source data survives
- provenance survives value replacement

### Adaptive scrolling

The Suno extractors learned that the useful scroll target may be a nested virtualized container rather than `window`. That principle remains relevant to Ideogram and other infinite creative galleries.

The browser collector is therefore a field tool, not the canonical archive interface.

### Offline recovery

Saved Suno HTML could be mined after the live page changed. Content Universe treats offline recovery as a primary capability:

```text
HAR
saved HTML
exported JSON / CSV
structured app state
```

should remain useful independently of the live platform.

## What Content Universe intentionally fixes

The historical Suno repo also demonstrated failure modes worth avoiding:

- multiple "ultimate/final" versions competing as canonical
- concatenated generations of scripts
- duplicated CSV utilities
- hard-coded local filesystem paths
- malformed merge/paste artifacts
- browser UI tightly coupled to extraction logic

Content Universe therefore separates:

```text
core
adapters
interfaces
storage
browser collectors
fixtures
archive/research evidence
```

## Suno migration direction

The initial `SunoExportAdapter` is deliberately modest. Future migration should happen in layers:

1. JSON export normalization
2. CSV normalization
3. saved HTML recovery
4. Next.js embedded-state recovery
5. historical richer-row merge compatibility
6. cover/audio asset manifests
7. lyrics/style metadata extraction
8. publication and video relationships
9. migration tools for existing master catalogs

The goal is one Content Universe containing both the music and the visual systems around it, not another generation of isolated `final-final-v10.js` scripts.
