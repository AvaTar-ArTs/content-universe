# Adapter Specification

Adapters translate platform-specific evidence into Content Universe entities and relationships.

## Required interface

Every adapter implements:

```python
class Adapter(ABC):
    name: str

    def supports(self, source: str | Path) -> bool: ...
    def harvest(self, source: str | Path) -> HarvestResult: ...
```

`HarvestResult` contains:

```text
records      canonical GenerationRecord list
graph        CreativeGraph
provenance   ProvenanceLedger
metadata     adapter/run metadata
warnings     non-fatal recovery warnings
```

## What belongs in an adapter

- source recognition
- platform identity extraction
- source-specific parsing
- stable ID normalization
- conservative graph edge creation
- source observations
- source-level warnings

## What does not belong in an adapter

- global persistence policy
- universal CLI behavior
- browser credentials
- platform-independent merge logic
- MCP protocol handling
- application UI

## Discovery vs enrichment

Prefer a two-stage design.

### Discovery

Fast, cheap, broad:

```text
ID
URL
response index
asset identity
visible title/prompt
observation source
```

### Enrichment

Slower and more structured:

```text
full prompt
expanded prompt
model
seed
reference collections
lineage
asset variants
engagement
platform metadata
```

This pattern came directly from the mature Suno extractor family and maps cleanly onto Ideogram.

## Stable selectors

For DOM adapters, prefer:

1. semantic `data-testid` / accessibility attributes
2. stable application URLs
3. embedded structured state
4. media URLs containing native IDs
5. generated CSS classes only as a last resort

## Source precedence

Adapters should surface evidence rather than deciding truth globally. The normal preference order is:

```text
structured API/JSON
captured structured responses
embedded app state
semantic DOM
heuristic DOM
```

But a lower-precedence source can still be the only source for a useful observation.

## Identity requirements

An adapter should identify the narrowest stable native ID available.

Avoid using:

- titles as identity
- array position without a parent request ID
- generated local filenames as identity
- prompt text hashes unless the platform provides no persistent ID

## Graph edge requirements

Only emit a typed edge when the source supports that relationship.

Good:

```text
generation A --produced--> response B
```

when response B appears in A's response list.

Bad:

```text
generation A --edit_of--> response C
```

because C appears somewhere in generic `references` without an edit-specific branch.

## Security requirements

Adapters must not:

- hard-code cookies or bearer tokens
- write raw HARs into the repository
- replay captured requests by default
- silently persist credentials
- scrape private data outside the user's supplied/authorized source

Authenticated transports are injected from outside the core.

## Recommended directory layout

```text
src/content_universe/adapters/<platform>/
├── __init__.py
├── har.py
├── html.py
├── profile.py
├── assets.py
├── models.py
└── ...
```

Not every platform needs every module.

## Testing contract

Every adapter should have at least:

- supports/recognition test
- canonical identity test
- sparse record test
- richer record test
- malformed/missing field test
- graph relationship test where applicable
- synthetic or sanitized fixture

Never make CI depend on a live third-party service.
