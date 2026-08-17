# MCP Interface

Content Universe exposes an optional MCP server backed by the local SQLite catalog.

## Install

```bash
python -m pip install -e '.[mcp]'
```

## Run

```bash
content-universe-mcp --db catalogs/avatararts.sqlite
```

## Tools

### `catalog_stats()`

Returns counts for generations, responses, assets, collections, profiles, graph edges, and provenance observations.

### `get_generation(request_id)`

Returns one canonical generation record.

### `get_response(response_id)`

Returns one canonical response record.

### `get_asset(asset_id)`

Returns one canonical asset record.

### `get_collection(collection_id)`

Returns one reference collection.

### `get_profile(key_or_handle)`

Returns a profile by internal user ID or handle.

### `search_prompts(text, limit=20)`

Searches normalized generation payloads. The first implementation uses SQLite `LIKE`; FTS5 is on the roadmap.

### `model_counts()`

Returns generation counts grouped by model version.

### `request_type_counts()`

Returns generation counts grouped by request type.

### `lineage(entity_key)`

Returns incoming and outgoing graph edges for a typed entity key.

Examples:

```text
generation:fixture-request-001
response:fixture-response-001
asset:some-asset-id
collection:some-reference-collection
```

### `provenance(entity_key)`

Returns observations describing where and when an entity was seen.

### `assets_for_response(response_id)`

Returns known asset representations attached to a response.

## Design boundary

The MCP server does not scrape Ideogram or Suno itself. It queries a catalog built by adapters and harvesting workflows.

That boundary matters because:

- agents do not need browser credentials
- the same catalog can be queried offline
- platform changes do not rewrite the MCP layer
- test fixtures remain deterministic
- browser/security concerns stay outside the agent protocol

## Suggested agent workflow

```text
HAR / HTML / export
      ↓
content-universe harvest
      ↓
local SQLite catalog
      ↓
content-universe-mcp
      ↓
agent / IDE / orchestration system
```

A future remote/service mode can sit above the same query contracts without changing canonical records.
