# Data Model

Content Universe keeps platform identity intact instead of flattening every creative artifact into a single row.

## Core entities

### Generation

A creation request or platform-level generation event.

Typical fields:

- `request_id`
- `request_type`
- original user prompt
- negative prompt
- caption / description
- seed
- model/version
- dimensions / aspect ratio
- style metadata
- platform references
- completion/error state
- one or more responses

### Response

One output produced by a generation. A request may produce several responses.

Typical fields:

- `response_id`
- `response_index`
- expanded/autoprompt
- primary asset URL
- format
- likes/engagement snapshot
- visibility
- platform-specific raw metadata

### Asset

A concrete media representation associated with a response or collection.

Examples:

- original PNG
- balanced Ideogram preview
- 2K representation
- Suno MP3
- cover image
- MP4 visualization
- storyboard frame

Assets remain separate because a response may have several representations.

### Collection

A platform-native reference collection or reusable asset set.

Examples:

- style reference collection
- character reference collection
- product reference collection

Collections may carry version IDs and member asset IDs.

### Profile

A platform identity such as an Ideogram public profile or future Suno account source.

A profile is not required for every record, because imported/offline artifacts may be detached from a live account.

## Entity keys

Graph/provenance systems use typed keys:

```text
generation:<request-id>
response:<response-id>
asset:<asset-id>
collection:<collection-id>
profile:<profile-id>
```

Typed keys prevent accidental collisions between unrelated ID namespaces.

## Relationships

Current edge types:

```text
produced
edit_of
variation_of
style_reference
character_reference
product_reference
upload_parent
member_of
```

Relationships are conservative. If the captured source only proves that a generation references an asset, Content Universe must not silently upgrade that relationship to `edit_of` without supporting evidence.

## Provenance

Every canonical entity can accumulate observations:

```json
{
  "source": "ideogram-har",
  "observed_at": "2026-08-17T02:00:00+00:00",
  "locator": "local-capture.har",
  "confidence": 1.0,
  "metadata": {}
}
```

A merged entity may therefore have evidence from:

- a profile API capture
- saved HTML
- a userscript observation
- an older export
- a later enrichment pass

The preferred value can change while the evidence history survives.

## Merge philosophy

The historical Suno tooling demonstrated the value of preferring richer rows during deduplication. Content Universe generalizes that behavior while preserving source history.

Rules:

1. Never change canonical identity because a later source is richer.
2. Fill missing fields from richer observations.
3. Deep-merge dictionaries.
4. Union list-like identifiers without duplicates.
5. Preserve platform-specific raw data.
6. Preserve provenance even when values are superseded.
7. Split response entities before comparing generation richness.

## Canonical vs raw

The canonical model intentionally stays compact. Platform-specific fields belong in `raw` until they prove useful across adapters.

This avoids a common extractor failure mode where the shared schema becomes a landfill of one-off platform keys.

## Storage

SQLite persists:

```text
generations
responses
assets
collections
profiles
graph_edges
provenance
universe_metadata
```

The JSON payload stored alongside indexed columns remains the source of truth for full-fidelity local recovery.
