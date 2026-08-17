# Content Universe

**Content Universe** is a provenance-aware creative harvesting, recovery, normalization, and catalog system for multimodal creator platforms.

The project grows out of the extraction/recovery patterns developed in the AvaTar-ArTs Suno tooling and generalizes them into a platform-independent core. Ideogram is the first adapter implemented against captured browser/HAR evidence.

## What this is

Content Universe separates acquisition from normalization and intelligence:

```text
browser DOM ─┐
HAR capture ─┼─> adapter -> canonical records -> merge/provenance -> catalog
saved HTML ──┤                                      |
API JSON ────┘                                      +-> JSON / JSONL / SQLite / MCP
```

The core design principles are:

- **structured sources first** — prefer API/JSON/HAR payloads over brittle CSS scraping
- **identity before flattening** — preserve request, response, asset, collection, and lineage IDs
- **staged enrichment** — discover cheaply, enrich deeply later
- **provenance-preserving merge** — richer records augment earlier records rather than blindly replacing them
- **offline recovery** — HAR, saved HTML, and exported JSON should remain useful when a live site changes
- **adapter architecture** — Suno, Ideogram, and future creative systems share the same harvesting core

## Ideogram discoveries implemented here

Captured Ideogram traffic shows a cursor-paginated public profile feed:

```text
GET /api/g/u/profile/c?display_handle=<handle>&sort_filter=DEFAULT
GET /api/g/u/profile/c?display_handle=<handle>&sort_filter=DEFAULT&cursor=<opaque-cursor>
```

Generation records may include:

- `request_id`
- `request_type`
- `responses[].response_id`
- `responses[].response_index`
- original and expanded/autoprompt text
- seed
- model version / URI
- dimensions and aspect ratio
- image resolution tier
- style metadata
- edit/style/character/product reference collections
- completion/error state
- engagement metadata

Gallery HTML also exposes useful identities such as:

```text
data-testid="image-grid-item-<generation-id>"
/g/<generation-id>/<response-index>
/assets/image/.../response/<response-id>@2k
```

These provide a DOM fallback when structured profile/API data is unavailable.

## Security

**Do not commit raw authenticated HAR files.** HAR captures can contain cookies, bearer tokens, account identifiers, request headers, and other session material.

Use them locally and export only sanitized fixtures or normalized records.

`.gitignore` intentionally excludes `*.har`, browser capture folders, cookies, tokens, and local catalogs.

## Current package

```text
src/content_universe/
  catalog.py            canonical records + provenance-aware merge
  ideogram.py           offline HAR/profile extraction
  cli.py                command-line entry point
```

### Install

```bash
python -m pip install -e .
```

### Inspect an Ideogram HAR

```bash
content-universe ideogram-har ideogram.ai-avatararts.har --summary
```

### Export normalized records

```bash
content-universe ideogram-har ideogram.ai-avatararts.har \
  --jsonl avatararts.generations.jsonl
```

The parser is intentionally offline-first: it reads already-captured HAR files and does not require browser credentials.

## Next adapters

- Suno profile/library recovery
- saved Ideogram HTML
- live browser userscript/extension bridge
- response metadata enrichment
- reference/lineage graph
- asset downloader
- SQLite catalog
- MCP query layer

## Why “Content Universe”

The final unit is not an image or song. It is a **creative object with identity, provenance, lineage, prompts, assets, references, and relationships**. Content Universe is the graph that keeps those pieces connected.
