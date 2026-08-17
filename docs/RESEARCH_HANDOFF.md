# Research & Engineering Handoff

This document records the research trail that produced Content Universe v0.3 so another developer or agent can continue without reconstructing the conversation that led here.

## Objective

Build a reusable creative recovery/catalog system by combining:

1. the mature extraction/recovery patterns from the AvaTar-ArTs Suno tooling,
2. direct evidence from captured Ideogram browser/network data,
3. a platform-independent provenance and lineage model,
4. higher-order creator entities such as projects, series, stories, characters, tracks, videos, and publications.

The result should not become another platform-specific “ultimate extractor.” Platform collectors are adapters around a shared creative graph.

---

## Raw research artifacts used during development

The following artifacts were supplied privately during research. **They should not be committed to this repository in raw form.**

### Ideogram

- `ideogram.ai2.har`
  - early Ideogram network capture
  - exposed model/config/category/metadata request families
- `Pasted text(20260817-020917).txt`
  - captured Explore/t-shirt generation JSON
  - showed complete generation records and structured/autoprompt examples
- `Pasted text(20260817-021255).txt`
  - saved/rendered Ideogram page HTML
  - exposed stable semantic DOM attributes, generation links, and asset URL identities
- `ideogram.ai-all.har`
  - wider application/network capture
  - confirmed model catalog/config and Explore traffic
- `ideogram.ai-avatararts.har`
  - capture of `https://ideogram.ai/@avatararts`
  - revealed the cursor-paginated profile generation feed

### Historical Suno work

Research reviewed prior AvaTar-ArTs Suno extractor history and repository evidence, including the `userscripts` family and artifacts such as:

- `Suno Extractor v8.0 (Ultimate Integrator)-8.0.user.js`
- earlier v7/v8/v9 extractor/dashboard generations
- `extract-suno.js`
- `LIVE_SUNO_EXTRACTOR.js`
- `universal-suno-extractor.js`
- `suno-extractor-utils.js`
- `compare-suno-exports.js`
- `combine-all-suno-exports.js`
- `merge-all-suno-sources.js`
- `merge-all-suno-intelligent.js`
- advanced/fixed/master extractor variants
- historical Python saved-HTML extractor using Next.js `__NEXT_DATA__` with HTML fallback

These names are recorded as research provenance, not as a requirement to copy historical code verbatim.

---

## Ideogram findings

### 1. Generation record shape

Captured generation objects included combinations of:

```text
user
user_prompt
user_negative_prompt
private
request_id
request_type
responses[]
creation_time_float
resolution
height
width
user_hparams
seed
aspect_ratio
model_version
model_uri
cover_response_id
autoprompt flags
completion/error state
sampling_speed
max_upscale_factor
image_resolution
expected_number_of_final_responses
character_reference_collection_ids
product_reference_collection_ids
style_reference_collection_ids
references
style_expert
caption
```

Responses included combinations of:

```text
response_id
prompt
response_index
format
num_likes
self_like
private
cover
pin_on_profile
is_autoprompt
references
```

### 2. Structured autoprompt

Some response prompts were not plain text. Ideogram expanded ordinary prompts into JSON-like composition specifications shaped around:

```text
high_level_description
compositional_deconstruction
  background
  elements[]
    type: obj | text
    text
    desc
```

Captured examples described:

- individual typography blocks
- object placement
- color values
- line weight
- rotation
- print techniques
- hierarchy
- texture
- background treatments

Engineering consequence: preserve **both** creator prompt and expanded response prompt. Do not overwrite one with the other.

### 3. Request / response identity

Saved HTML showed generation URLs shaped as:

```text
/g/<generation-or-request-id>/<response-index>
```

and image assets shaped as:

```text
/assets/image/<representation>/response/<response-id>@<resolution>
```

Semantic DOM attributes included:

```text
data-testid="image-grid-item-<generation-id>"
data-testid="generation-hover-tool-bar"
data-testid="desktop-prompt-box-surface"
data-testid="desktop-generation-box"
data-testid="prompt-text-field"
data-testid="model-selection-config-container"
data-testid="model-selection-menu-container"
```

Engineering consequence: the DOM can bootstrap request → response identity without relying on generated CSS class names.

### 4. Profile archive endpoint

The `@avatararts` capture revealed:

```text
GET /api/g/u/profile/c?display_handle=avatararts&sort_filter=DEFAULT
```

with later pages using:

```text
&cursor=<opaque-cursor>
```

Captured responses returned another cursor, proving cursor traversal rather than a one-page snapshot.

Engineering consequence: profile/API recovery is preferred over simulating infinite DOM scrolling for deep archive recovery. The userscript remains a field/fallback collector.

### 5. Public profile snapshot

At capture time, public profile information for `avatararts` reported approximately:

```text
generations: 2183
likes: 25
join date: September 1, 2023
```

Treat these as capture-time observations, not permanent facts.

### 6. Model catalog

Captured model catalog data exposed capability flags such as:

```text
supports_inpaint
supports_canvas
supports_color_palette
supports_negative_prompt
supports_rendering_speed
supports_tiling
supports_style_reference
supports_custom_aspect_ratio
supports_character_reference
supports_product_reference
supports_flash_rendering_speed
supports_external_api
auto_background_removal
is_custom_model
is_primary_model
access_level
available_resolution_tiers
```

Engineering consequence: model capabilities should be parsed as data rather than hard-coded into UI logic.

### 7. Other observed request families

Captured traffic included request families such as:

```text
/api/models/catalog
/api/generations/allAvailableResolutions
/api/generations/retrieveColorPalettes
/api/generations/getRequestCost
/api/generations/getRequestStats
/api/images/batch_retrieve_metadata
/api/v2/category
/api/category/list
/api/v2/category/featured-t-shirt/assets
/api/f/p/cluster/tshirt_v8
/api/canvases/list
/api/users/public_info/{handle}
/api/users/settings
/api/account/user_task_quota_stats
/api/account/subscriptionStatus
/api/organizations
/api/announcements/active-banner
```

These are **observed internal web-application surfaces**, not promises of a stable public API. Do not treat them as supported contracts without current verification.

### 8. Browser networking caveat

Saved Ideogram HTML showed Ideogram itself wrapping `window.fetch` to handle Cloudflare Turnstile challenge/retry behavior.

Engineering consequence: the Content Universe userscript deliberately avoids replacing `window.fetch`. Passive DOM observation and local HAR analysis are safer and less fragile. A future browser extension may use DevTools/network APIs instead.

---

## Suno lessons carried forward

### Canonical accumulator

Historical pattern:

```text
Map<song UUID, song record>
```

Content Universe evolution:

```text
request_id -> generation
response_id -> response
asset_id -> asset
collection_id -> collection
```

### Staged enrichment

Historical Suno extractors first collected lightweight rows and later fetched lyrics/tags/summary detail.

Generalized pattern:

```text
discover
  ↓
normalize
  ↓
enrich
  ↓
merge
  ↓
graph
  ↓
persist
```

### Adaptive scrolling

Historical Suno collectors learned to locate nested virtualized scroll containers, monitor whether the canonical ID count changed, nudge backward to retrigger lazy loading, and stop after repeated idle cycles.

The Ideogram userscript now inherits that pattern.

### Intelligent richer-row merge

The strongest historical backend idea was not a particular browser UI. It was multi-source recovery:

```text
scan exports / saved pages
       ↓
identify canonical UUID
       ↓
deduplicate
       ↓
prefer richer metadata
       ↓
retain master catalog
```

Content Universe keeps that principle while adding provenance so superseded observations are not erased.

### Offline recovery

Historical saved Suno HTML and `__NEXT_DATA__` recovery proved that creator data should remain recoverable after UI changes.

Content Universe makes HAR, saved HTML, JSON, CSV, and browser exports first-class adapter inputs.

### Historical failure modes intentionally avoided

Prior extractor evolution also exposed architectural problems:

- many competing “final/ultimate” script versions
- duplicated CSV helpers
- hard-coded local filesystem paths
- pasted/concatenated versions
- malformed optional chaining / merge damage in some historical files
- browser UI and extraction logic tightly intertwined

Content Universe therefore separates adapters, core, storage, browser collectors, interfaces, schemas, fixtures, and docs.

---

## Architecture decisions

### Decision A: request and response are separate entities

Reason: one generation can produce multiple responses; responses can later participate in edit/remix/reference lineage.

### Decision B: asset is separate from response

Reason: one response may have original, balanced, resized, video, audio, cover, or other representations.

### Decision C: provenance is separate from raw payload

Reason: raw payload says what a source contained. Provenance says **where and when** the canonical entity was observed.

### Decision D: relationships are conservative

Reason: generic references should not automatically become `edit_of` or `style_reference` unless the source branch actually establishes that relationship.

### Decision E: browser collectors do not own credentials

Reason: platform networking/authentication changes frequently and raw browser state is sensitive.

### Decision F: higher-order creator intent is explicit

Reason: a platform cannot know that an image is the cover of a manga series, a song is its theme, or a character belongs to a story unless that relationship is authored elsewhere.

Content Universe manifests provide that explicit layer.

### Decision G: live transports are injected

Reason: the profile cursor walker should work with browser bridges, fixture transports, or future API clients without the core storing session state.

### Decision H: external adapters use entry points

Reason: Content Universe should grow into Leonardo, ComfyUI, Drive, GitHub, video generators, and other systems without turning the core registry into a monolith.

---

## What is implemented in v0.3

### Core

- canonical records
- completeness merge
- provenance ledger
- graph
- cross-media creative entities
- ContentUniverse aggregate
- SQLite persistence
- JSON/JSONL/CSV/full-universe exports
- FTS5 optional indexing
- query layer
- audits
- batch pipeline
- manifest system
- plugin entry points

### Ideogram

- HAR
- saved HTML
- browser JSON export
- cursor walker contract
- model capabilities
- asset manifests
- public asset download boundary
- structured prompt decomposition
- endpoint inventory
- HAR sanitizer
- adaptive userscript

### Suno

- JSON export
- flexible CSV
- saved HTML
- Next.js state
- song-link fallback

### Interfaces

- CLI
- MCP
- TUI
- browser userscript
- Docker MCP image

---

## Remaining high-value Ideogram captures

The architecture does not depend on these, but each would make the Ideogram adapter more complete:

1. **Fresh text-to-image generation**
   - record before submit
   - submit disposable prompt
   - wait for every output to finish
   - stop capture
   - goal: exact request payload, polling/completion behavior, final result contract

2. **Edit/remix**
   - goal: authoritative source-parent and edit relationship shape

3. **Style reference generation**
   - goal: request-side collection binding and version semantics

4. **Character reference generation**
   - same goal for character references

5. **Product reference generation**
   - same goal for product references

6. **Prompt Builder**
   - goal: direct transformation contract from rough prompt to expanded prompt

7. **Image Studio / Canvas**
   - goal: canvas/document entity and operation lineage

Do not upload authentication secrets intentionally. Keep raw captures private.

---

## Recommended next engineering work

### Highest priority

1. reference collections → canonical `CollectionRecord`
2. cross-generation edit/remix lineage resolution
3. Suno historical master-catalog migration
4. FTS/search analytics over a real local archive
5. link CLI for harvested IDs ↔ creative manifest entities

### Next platform adapters

- Leonardo
- ComfyUI outputs/workflows
- generic image-generation manifest
- video generation
- GitHub creative repositories
- Google Drive / local creator filesystem

### Creator-OS layers

- character bible schema
- visual style bible schema
- storyboard/comic layout entities
- publication/release records
- marketplace/product records
- campaign bundles
- handoff dossier generation
- dependency/lineage visualization

---

## Security reminder

Raw captures are research evidence, not repository assets.

Before publishing any derived fixture:

```text
copy
sanitize
minimize
search for secrets
manual review
commit only the smallest useful fixture
```

Never rely on `.gitignore` as the only protection against secret leakage.
