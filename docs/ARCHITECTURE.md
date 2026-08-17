# Architecture

Content Universe is the durable identity, provenance, lineage, recovery, and creative-state substrate for a larger creator operating system. It is **not** merely a scraper collection, and it is also **not** intended to replace the structured-authoring and provider-runtime ideas previously developed under iDeoMine / CreativeOS.

See [`CONVERSATION_SAVEPOINT_AUDIT.md`](CONVERSATION_SAVEPOINT_AUDIT.md) for the chronological reconstruction that recovered these boundaries.

## Product/layer boundaries

The design uses several names deliberately rather than treating them as synonyms:

- **Content Universe** — umbrella durable graph/catalog/runtime substrate. Owns identity, provenance, lineage, persistence, recovery, creator entities, durable asset records, and shared interfaces.
- **CreativeOS** — provider-neutral authoring/orchestration layer above Content Universe. Owns normalized creative intent, structured authoring, workflows, provider routing, evaluation, approvals, and cross-provider behavior.
- **iDeoMine** — deep Ideogram-native integration/workflow layer. Owns Ideogram-specific capabilities, semantics, state, structured-prompt dialect, references, collections, datasets/models, and provider-native operations when legitimate supported transport exists.
- **Prompt Builder** — structured authoring subsystem. Owns creator brief → scene/prompt structure and media/description → reusable structured scene transformations.
- **Reference Genome** — reusable creative memory: canon, character identity anchors, style rules, palettes, typography, approved references, exclusions, and approved-output/training feedback.
- **Asset Graph** — the durable relationship substrate implemented within Content Universe's graph/persistence layer.
- **Skills** — procedural knowledge/workflow recipes that may operate above the runtime without becoming provider contracts.

These boundaries prevent a recovery parser from accidentally becoming a live provider client, and prevent a provider API wrapper from becoming the canonical creative data model.

## Two directions, one universe

Content Universe must support both **recovery** and **authoring**.

```text
                       CONTENT UNIVERSE
                              │
          ┌───────────────────┴───────────────────┐
          │                                       │
  EVIDENCE / RECOVERY                       CREATIVE AUTHORING
          │                                       │
 HAR · HTML · CSV · JSON                    Creative Brief
 browser collectors                         Canon / Character
 archive/profile feeds                      Style / References
          │                                       │
          ▼                                       ▼
   Recovery Adapters                         Prompt Builder
          │                                       │
          └─────────────────┐       ┌─────────────┘
                            ▼       ▼
                       CANONICAL GRAPH
            entities · assets · provenance · lineage
                            │
                ┌───────────┴───────────┐
                ▼                       ▼
         CreativeOS Runtime       Reference Genome
                │                       ▲
         Workflow / Router              │
                │                       │
      Provider Backend/Dialect          │
                │                       │
 iDeoMine · Leonardo · FLUX · ...      │
                │                       │
                ▼                       │
      Generation / Transformation      │
                │                       │
                ▼                       │
       Evaluation / Approval ───────────┘
                │
                ▼
         Durable Asset Graph
```

The current v0.3 repository is strongest on the left-hand recovery/catalog branch. The authoring/provider-runtime branch is being restored as an explicit roadmap rather than being implied by generic “Creator OS” language.

## Recovery system layers

```text
┌──────────────────────────────────────────────────────────────┐
│  Acquisition                                                 │
│  HAR · saved HTML · JSON/CSV · userscript · archive feeds   │
└──────────────────────────────┬───────────────────────────────┘
                               ▼
┌──────────────────────────────────────────────────────────────┐
│  Recovery adapters                                            │
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
│  SQLite · FTS · JSON/JSONL/CSV · Mermaid · dataset packs     │
└──────────────────────────────┬───────────────────────────────┘
                               ▼
┌──────────────────────────────────────────────────────────────┐
│  Recovery/query interfaces                                    │
│  CLI · query MCP · query TUI · browser collector             │
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

## Semantic operation integrity

The recovered CreativeOS/iDeoMine design treats provider operations as **intent contracts**. Future live provider backends must preserve these distinctions:

```text
GENERATE           new media from creative intent
EDIT               modify referenced media
REMIX              derive a variation from one parent
REFRAME            change framing/canvas around a parent
UPSCALE            increase resolution/detail of a parent
REMOVE_BACKGROUND  create background-removed derivative
DESCRIBE            inspect/describe media
```

A failure in one operation is not permission to silently execute another. Source-cardinality requirements and parent/derivative lineage belong in provider-neutral validators before provider transport is introduced.

## Recovery adapters vs provider backends

These are intentionally different interfaces.

### Recovery Adapter

Reads existing evidence/history:

```python
supports(source) -> bool
harvest(source) -> HarvestResult
```

Examples:

- Ideogram HAR
- saved Ideogram HTML
- browser observation export
- Suno CSV/JSON/HTML

A recovery adapter does not perform live creative mutations.

### Provider Backend

Future CreativeOS contract for supported live operations:

```text
capabilities()
execute(OperationRequest) -> OperationResult
status(job_id)
```

Backends own supported authentication/transport, retries, provider response normalization, cost/rate-limit metadata, and live operation execution. They do **not** become the canonical creative graph.

### Provider Dialect

Translates provider-neutral structured intent into provider-specific prompt/reference/model semantics while preserving the original structured intent and prompt lineage.

### Workflow

Composes Prompt Builder, Reference Genome, provider operations, persistence, evaluation, and approval. Workflows are not recovery pipelines.

This distinction matters because the current `pipeline.py` orchestrates **ingestion/recovery**, while the older CreativeOS Workflow Engine orchestrated **creative actions**.

## Structured authoring model to restore

The authoring branch is expected to add these provider-neutral structures:

```text
PromptManifest
PromptLineage
SceneGraph
SceneElement
TypographyLayer
StyleStack
StyleDNA
ReferenceGenome
EvaluationRecord
ApprovalRecord
```

### Prompt Builder taxonomy

The earlier design grouped these methods under Prompt Builder:

```text
build
import
describe
deconstruct
magic_prompt
layerize_text
compose
reference
edit
enhance
validate
localize
reflow
export
```

Some are local/provider-neutral transformations; others require legitimate provider capabilities. Provider-backed operations must never be simulated while being presented as though a provider call happened.

### SceneGraph

The intended scene representation includes:

- high-level description,
- background,
- typed elements,
- object/text/graphic/panel/environment/effect/region types,
- bounding boxes/anchors where known,
- references,
- provider metadata,
- typography layers for text elements.

The existing `promptlab.py` structured-autoprompt parser is a useful **import source** for SceneGraph but is not itself the complete Prompt Builder.

### Style representation

Style must not collapse into a single scalar. The recovered design distinguishes:

- prompt-keyword style,
- provider model mode,
- provider preset,
- image reference,
- saved style,
- quick reference,
- custom model,
- portable `StyleDNA`.

## Two graphs, one system

Content Universe uses one generic `CreativeGraph`, but conceptually it contains multiple relationship families.

### Platform provenance/lineage

```text
generation --produced--> response
request --style_reference--> collection
request --character_reference--> collection
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

### Authoring/runtime relationships

Future examples:

```text
brief --expanded_into--> prompt_manifest
prompt_manifest --rendered_as--> provider_dialect
response --evaluated_by--> evaluation
asset --approved_as--> reference_genome_entry
asset --trained_into--> custom_model
```

The same durable graph lets explicit creator intent, recovered platform history, and future live workflow results coexist without flattening their semantics.

## ContentUniverse aggregate

`ContentUniverse` currently groups:

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

This is the current in-memory composition root. Future authoring/runtime state should extend this substrate rather than create a disconnected second database.

## Ideogram recovery adapter family

```text
ideogram/
├── har.py              offline captured JSON recovery
├── html.py             saved semantic DOM recovery
├── browser_export.py   userscript observation import
├── profile.py          cursor URL + transport-independent walker
├── models.py           model capability extraction
├── references.py       reference collections/assets into graph entities
└── assets.py           asset parsing/manifests/public downloader
```

The legacy-compatible `content_universe.ideogram` module contains the low-level generation/HAR normalization functions used by the adapter family.

A future **iDeoMine provider backend** is a separate concept from these recovery adapters.

## Suno recovery adapter family

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
profile/archive record
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

Verified provider facts, working interpretations, and unresolved claims should also remain distinguishable in engineering handoffs.

## Persistence and durable assets

SQLite stores both indexed columns and full JSON payloads.

Current tables include:

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

This gives the project an evolvable metadata schema without throwing away new platform fields.

However, remote provider URLs are **not** intended to become the permanent asset store. The durable-asset roadmap requires content hashes, stable object locators, MIME/size/dimensions, integrity verification, and optional mirroring/object storage while retaining provider URLs as provenance.

## MCP boundaries

### Current query MCP

The existing MCP server queries the durable catalog. It does not browse creator platforms or own provider credentials.

That keeps recovery/query behavior deterministic and useful across CLI/TUI/scripts.

### Future CreativeOS semantic MCP

A future runtime MCP surface may expose authoring/workflow/provider operations, but it must delegate through provider backends and semantic validators rather than directly coupling MCP tools to provider HTTP implementations.

## Browser boundary

The userscript is an observational field collector. It intentionally avoids hooking the platform's authentication/network stack.

It borrows mature Suno ideas:

- canonical ID map,
- adaptive scrolling,
- lazy-load nudging,
- idle-stop,
- session resume,
- passive mutation observation,
- export.

A future browser extension / DevTools collector may capture richer network evidence without turning authenticated browser state into public fixtures.

## External plugins

Python entry points under:

```text
content_universe.adapters
```

register **recovery adapters** today.

Future provider-backend plugins should use a separate entry-point namespace so live mutation providers and evidence parsers cannot be confused merely because both integrate a platform.

## Security boundary

Raw authenticated captures are private local evidence.

Public repository inputs should be:

- synthetic fixtures,
- manually reviewed sanitized fixtures,
- normalized records,
- endpoint/schema summaries with secrets/query values removed.

Provider backends must add their own live-transport security: supported auth, secret isolation, SSRF/path controls where applicable, MIME/size validation, redirect policy, rate limits, and normalized errors.

No raw browser cookies, bearer tokens, or private HARs belong in source control.

## Non-negotiable invariants

The chronological audit recovered these rules from earlier iDeoMine/CreativeOS work. They should progressively become executable contracts/tests:

1. Never silently substitute edit/remix/reframe/upscale/generate operations.
2. Never claim a provider operation occurred when only mock/local logic ran.
3. Never make provider URLs the durable system of record.
4. Never overwrite the original creator prompt when enhancing it.
5. Never collapse authoring-only references into generation references.
6. Never make Ideogram's provider JSON the provider-neutral canonical format.
7. Never flatten repeated character instances when identity linkage exists.
8. Never turn collection cleanup into permanent asset deletion implicitly.
9. Preserve source IDs and parent/derivative lineage on transformations.
10. Surface partial failures in bulk workflows.
11. Keep provider-specific behavior behind provider backends/dialects.
12. Record verified facts, inferences, and unresolved claims separately.
