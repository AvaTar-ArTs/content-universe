# Conversation Save-Point Audit

**Audit date:** 2026-08-17  
**Repository:** `AvaTar-ArTs/content-universe`  
**Baseline reviewed:** `main` at `c7bb36202ffa6f20c360dad1c6e7380348b7ed92`  
**Purpose:** reconstruct the design evolution from the beginning of the Ideogram audit thread and earlier iDeoMine/CreativeOS work, then compare every major checkpoint against what actually exists in Content Universe.

This document is intentionally stricter than a roadmap. A roadmap says what we want. This audit says **what was said, what was discovered, what was built, what was lost between iterations, what is only partially represented, and what must not be silently forgotten.**

---

## 1. Sources used for this audit

### Current Ideogram audit thread

The exported `Ideogram Generation Audit` conversation was parsed chronologically rather than reconstructed from memory. The export contained 24 textual user/assistant messages through the beginning of the large Content Universe expansion.

The visible user checkpoints in that export were:

1. initial Ideogram HAR + generation-text bundle,
2. `review my history for suno-extractor and see if its possible to adapt`,
3. `what else do you require`,
4. `mine https://ideogram.ai/@avatararts`,
5. `@GitHub https://github.com/AvaTar-ArTs/content-universe.git`,
6. `clearly you should add so very much more...`.

The active conversation after the export continued the implementation, CI repair, dataset-pack work, reference collection enrichment, and the present audit request.

### Earlier iDeoMine / CreativeOS work

Also compared:

- `iDeoMine-Handoff.md`
- `iDeoMine_MCP_vs_Ideogram.json`
- `MASTER_REVIEW.md`
- historical Suno extractor audit/history

These earlier artifacts matter because Content Universe did **not** begin from zero conceptually. A provider/runtime/authoring architecture had already been worked out before the new recovery-focused repository existed.

---

# 2. Save points

## SP-00 — Earlier Ideogram Genome / Suno-style collector direction

Before the current audit thread, the design direction already included a Suno-style Ideogram collector with:

- floating browser controls,
- auto-scroll harvesting,
- resume/incremental state,
- image identity maps,
- blueprint/composition extraction,
- motif analysis,
- character/typography state,
- prompt evolution,
- an eventual DevTools/network collector path.

### Current repository parity

**Implemented:**

- adaptive Ideogram userscript,
- semantic generation/response identity,
- session resume,
- lazy-load nudging,
- prompt decomposition,
- graph/provenance.

**Still missing from the older vision:**

- blueprint engine as a first-class model,
- motif engine,
- reusable visual/character/typography genome abstractions,
- prompt-evolution intelligence beyond raw lineage,
- Chrome DevTools MCP/browser-extension network collector,
- automatic incremental enrichment after DOM discovery.

**Conclusion:** the recovery mechanics survived. The higher-order visual-intelligence vocabulary mostly did not.

---

## SP-01 — iDeoMine MCP: provider semantics and state

The August 16 handoff established iDeoMine as a **stateful creative operating layer**, not a generate-image wrapper.

The important provider-level concepts were:

- generate,
- edit,
- remix,
- reframe,
- upscale,
- background removal,
- history/status,
- uploads,
- describe,
- collections and collection membership,
- datasets,
- model training and model discovery,
- organization context.

It also established these hard rules:

- edit is not remix,
- remix is not fresh generation,
- reframe is not regenerate,
- upscale must preserve source lineage,
- a failed operation must not silently turn into a different operation,
- deletion of a collection and deletion of contained assets are different intentions,
- provider auth belongs behind a backend boundary,
- do not fake OAuth.

### Current repository parity

**Strongly preserved:**

- identity/provenance/lineage philosophy,
- adapter boundary,
- no credential ownership in the browser collector,
- persistent state through SQLite,
- collection entities as data.

**Not migrated:**

- provider operation contracts,
- semantic transform invariants,
- backend execution boundary (`MockBackend`, `RemoteMCPBackend`, future provider backend),
- generation/edit/remix/reframe/upscale tool surface,
- organization context,
- dataset/training state,
- custom-model lifecycle,
- live collection CRUD/membership operations,
- job/history/status execution model.

### Important distinction

Content Universe currently models **observed provider history**. The earlier iDeoMine layer modeled **provider actions an agent could intentionally perform**.

Those are complementary systems and should not be treated as interchangeable.

---

## SP-02 — CreativeOS master consolidation

The CreativeOS master review defined the larger product split:

- **iDeoMine** — deep Ideogram-native provider/workflow depth,
- **CreativeOS** — provider-neutral headless runtime,
- **Prompt Builder** — structured authoring,
- **Reference Genome** — reusable canon/defaults/creative memory,
- **Skills** — procedural workflow knowledge,
- **Asset Graph** — durable creative state and lineage,
- **MCP/TUI/Web/CLI/REST/A2A** — interfaces over the same runtime.

Canonical pipeline:

```text
Creative Brief
      ↓
Canon / Character / Style / References
      ↓
Prompt Builder
      ↓
Scene Graph + Prompt Lineage
      ↓
Provider Dialect
      ↓
Generation / Edit / Structure
      ↓
Structured Design Asset
      ↓
Asset Graph
      ↓
Evaluation / Continuity
      ↓
Approved Outputs
      ↓
Reference Genome / Training feedback
```

### Current repository parity

| CreativeOS concept | Current Content Universe | Status |
|---|---|---|
| Asset Graph | `CreativeGraph`, SQLite edges, provenance | strong partial |
| durable records | SQLite + raw JSON | implemented |
| Prompt Builder | `promptlab.py` decomposition only | partial |
| SceneGraph | no typed scene graph | missing |
| PromptLineage | generation lineage exists; authoring lineage does not | partial |
| TypographyLayer | raw prompt element fields only | missing |
| StyleStack | no equivalent | missing |
| StyleDNA | no equivalent | missing |
| Reference Genome | no equivalent | missing |
| provider capability registry | Ideogram model capability parser only | partial |
| provider registry/router | adapter discovery is input recovery, not execution routing | missing |
| workflow engine | batch ingestion pipeline is not creative workflow orchestration | missing |
| evaluation/continuity | no evaluator model | missing |
| approval gates | no approval/status model | missing |
| mock/live provider backends | absent | missing |
| remote MCP federation | absent | missing |
| TUI provider control deck | current TUI is catalog/query oriented | regressed scope |
| semantic MCP generation tools | current MCP is catalog/query oriented | regressed scope |
| Web / REST / A2A | future only | missing |

### Conclusion

The biggest conceptual omission in Content Universe is **not another extractor feature**. It is the unmerged CreativeOS authoring/orchestration layer.

---

## SP-03 — Initial Ideogram HAR + generation-object audit

The first current-thread bundle established that an Ideogram generation is a rich structured document, not just a prompt plus PNG.

Observed fields included:

- request/response identities,
- original and negative prompt,
- expanded/autoprompt,
- model/version URI,
- seed,
- dimensions/aspect ratio,
- resolution tier,
- sampling/rendering speed,
- expected response count,
- cover response,
- upload parent,
- style/character/product reference collections,
- likes/profile state,
- structured composition JSON.

Observed request families included:

- model catalog,
- available resolutions,
- color palettes,
- batch response metadata,
- categories/clusters,
- canvas listing,
- quota/cost/stats,
- profile/public info,
- organizations.

### Current repository parity

**Implemented:**

- recursive HAR generation extraction,
- request/response separation,
- raw payload preservation,
- structured prompt decomposition,
- model capability parser,
- endpoint inventory,
- reference collection enrichment,
- asset parsing,
- provenance.

**Partial / missing:**

- resolution registry parser,
- color-palette registry parser,
- full batch-metadata enrichment workflow,
- direct indexed fields for several important generation properties currently retained only in `raw`,
- organization normalization,
- cost/quota observation models,
- canvas/document entities,
- social/profile engagement history.

### Canonical-schema gap

`GenerationRecord` currently indexes a useful subset of the generation object but leaves properties such as `cover_response_id`, `sampling_speed`, `max_upscale_factor`, `can_upscale`, `expected_number_of_final_responses`, some upload-parent state, and several provider flags only inside `raw`.

That is safe for preservation but weak for querying, analytics, and model-aware workflow policy.

---

## SP-04 — Suno Extractor adaptation

This was a pivotal architectural checkpoint.

The reusable Suno pattern was identified as:

```text
DISCOVER
  ↓
ACCUMULATE
  ↓
ENRICH
  ↓
NORMALIZE
  ↓
DEDUPE
  ↓
EXPORT
  ↓
CATALOG / ASSETS / PIPELINE
```

The best Suno ideas were:

- canonical-ID `Map`,
- adaptive scrolling,
- lightweight discovery before deep enrichment,
- controlled concurrency,
- retries/delays,
- resume/autosave,
- intelligent richer-row merge,
- offline HTML recovery,
- CSV/JSON export,
- generated asset downloader,
- master-catalog consolidation.

### Current repository parity

**Implemented:**

- canonical identity maps,
- adaptive Ideogram userscript,
- session resume,
- richer-record merge,
- offline adapters,
- JSON/CSV/SQLite export,
- Suno JSON/CSV/HTML/`__NEXT_DATA__` recovery.

**Still missing as reusable core machinery:**

- generic staged enrichment queue,
- reusable worker/concurrency pool,
- retry/backoff policy objects,
- enrichment checkpoint/resume state,
- partial-failure model for batch enrichment,
- historical Suno master-catalog migration command,
- cover/audio asset manifest migration,
- Suno browser-export bridge.

### Conclusion

The repo inherited the Suno **recovery philosophy** more completely than it inherited the Suno **enrichment runtime**.

---

## SP-05 — Ideogram saved HTML / DOM checkpoint

The saved Ideogram page established stable-looking semantic hooks:

- `data-testid="image-grid-item-..."`,
- `/g/<request>/<response-index>`,
- `/response/<response-id>@<resolution>`,
- `data-feed`,
- prompt/model-selection test IDs,
- lazy-loaded image behavior.

It also showed Ideogram wrapping `window.fetch` for Cloudflare challenge handling, which led to the decision **not** to monkey-patch browser auth/network state in the userscript.

### Current repository parity

**Implemented well:**

- stable identity extraction,
- request → response graph edges,
- passive MutationObserver collector,
- feed extraction in userscript,
- fetch-hook avoidance,
- saved-HTML adapter.

**Missed details:**

- saved-HTML adapter does not currently extract engagement/like counts,
- saved-HTML adapter does not retain feed context,
- model-selection/prompt-box state is recognized in research but not modeled,
- browser export does not yet capture visible prompt/model settings,
- DevTools/browser-extension network capture remains unimplemented.

---

## SP-06 — `ideogram.ai-all.har`

The larger HAR confirmed that the web application exposes a broad internal surface beyond generation, including configuration, model, canvas, account, category and asset traffic.

### Current repository parity

The network-inventory/sanitizer approach is correctly conservative: these internal routes are treated as observed evidence, not a public/stable API.

**Still worth adding:**

- typed endpoint evidence records,
- capture-to-fixture minimization command,
- endpoint schema diff between captures,
- version/change detection for internal request families.

---

## SP-07 — `@avatararts` profile HAR

The profile capture revealed the most important archive shortcut:

```text
/api/g/u/profile/c?display_handle=avatararts&sort_filter=DEFAULT
```

with opaque cursor pagination.

The capture-time profile snapshot reported approximately 2,183 generations.

### Current repository parity

**Implemented:**

- profile cursor-page extraction from HAR,
- transport-independent cursor walker contract,
- profile record model.

**Not yet completed:**

- real full-archive crawl into Content Universe,
- count reconciliation: requests vs responses vs assets,
- enrichment of the full corpus with batch metadata,
- archive analytics over the real corpus,
- durable local asset mirroring,
- prompt/style/model evolution reports across the account history.

### Important next real-data test

The architecture has mostly been exercised against synthetic fixtures. The strongest next pressure test remains: ingest the accessible `@avatararts` archive into a local catalog and measure what breaks or remains ambiguous.

---

## SP-08 — Empty `content-universe` repository

The repository was intentionally initialized as a shared Creative Harvest / Content Universe core rather than an `ideogram-extractor` project.

Initial files were deliberately small:

- `catalog.py`,
- `ideogram.py`,
- `cli.py`,
- tests,
- security exclusions.

### Correct decision preserved

The repository should remain an umbrella system. Ideogram and Suno are adapters/domains, not the product boundary.

### What the first scaffold omitted

At this point the repo still lacked most of the previously designed CreativeOS authoring/runtime pieces. The later expansion solved storage/recovery/graph concerns but did not revisit that older runtime inventory deeply enough.

---

## SP-09 — Large Content Universe expansion

The expansion added substantial real engineering:

- adapter protocol and plugins,
- Ideogram HAR/HTML/browser/profile/model/assets/reference adapters,
- Suno CSV/JSON/HTML adapters,
- `ContentUniverse` aggregate,
- provenance ledger,
- graph,
- SQLite storage/query,
- FTS5 helper,
- manifests,
- dataset pack,
- CLI,
- MCP query server,
- TUI,
- userscript,
- sanitizer/network inventory,
- synthetic fixtures,
- schemas,
- CI/docs/security.

CI initially caught a saved-HTML response-index bug. The HTML context logic was fixed. The subsequent Python 3.11/3.12/3.13 jobs all passed install, Ruff, pytest and compile.

### Current problem

This expansion made Content Universe a credible **recovery/catalog platform**, but because the work accelerated from the new thread, it effectively re-derived a new architecture without fully importing the already-designed CreativeOS runtime.

That is the central finding of this audit.

---

# 3. What Content Universe is today

Today the repository is strongest at:

```text
CAPTURE / IMPORT
      ↓
NORMALIZE
      ↓
IDENTITY RESOLUTION
      ↓
RICHER-RECORD MERGE
      ↓
PROVENANCE
      ↓
LINEAGE / GRAPH
      ↓
PERSIST / QUERY / EXPORT
```

It answers:

> What creative artifacts exist, where did they come from, what IDs/metadata do they carry, and how are they related?

That is useful and real.

---

# 4. What the earlier architecture also intended

The older CreativeOS/iDeoMine work additionally answered:

```text
CREATIVE INTENT
      ↓
CANON / CHARACTER / STYLE / REFERENCES
      ↓
STRUCTURED AUTHORING
      ↓
PROVIDER ROUTING + SEMANTIC OPERATION
      ↓
GENERATION / EDIT / REMIX / REFRAME / UPSCALE
      ↓
EVALUATION / APPROVAL
      ↓
ASSET GRAPH
      ↓
REFERENCE / TRAINING FEEDBACK
```

It answers:

> What should we create next, with which constraints and provider capability, how do we preserve intent between transformations, and how do we decide what becomes approved creative memory?

Content Universe should eventually support **both directions**.

---

# 5. Missing migration inventory

## P0 — architectural identity

### 5.1 Restore explicit product/layer boundaries

The repo needs an explicit statement that:

- Content Universe is the umbrella durable graph/catalog/runtime,
- CreativeOS is the provider-neutral authoring/orchestration layer,
- iDeoMine is the deep Ideogram-native adapter/workflow layer,
- Prompt Builder is structured authoring,
- Reference Genome is reusable creative memory,
- Asset Graph is the persistent relationship substrate.

Without this, future agents can continue growing the recovery code while unknowingly abandoning the older design.

### 5.2 Restore semantic operation contracts

Create canonical operations for:

- generate,
- edit,
- remix,
- reframe,
- upscale,
- background removal,
- describe,
- structured/layerized operations.

These should be intent contracts, not provider HTTP wrappers.

### 5.3 Restore backend/provider execution boundary

Recovery adapters answer `harvest(source)`.

Creative execution needs a separate boundary such as:

```text
ProviderRegistry
ProviderCapabilities
ProviderBackend
ProviderDialect
OperationRequest / OperationResult
```

Do **not** overload recovery adapters with live mutation responsibilities.

---

## P1 — structured authoring

### 5.4 Prompt Builder

`promptlab.py` is currently an extractor/decomposer. It is not the older Prompt Builder.

Restore a method taxonomy including:

- build,
- import,
- describe,
- deconstruct,
- magic_prompt,
- layerize_text,
- compose,
- reference,
- edit,
- enhance,
- validate,
- localize,
- reflow,
- export.

Provider-backed methods must remain explicit and must not be simulated as though the provider ran.

### 5.5 SceneGraph + TypographyLayer

Add typed scene entities for:

- background,
- object,
- text,
- graphic,
- panel,
- environment,
- effect,
- region,
- bounding boxes/anchors,
- typography layers.

The current structured-prompt parser already exposes enough raw material to seed this model.

### 5.6 PromptLineage

Track:

- original creator brief,
- enhanced prompt,
- provider dialect,
- provider-expanded/autoprompt,
- revision deltas,
- localized/reflowed forms,
- image-derived descriptions.

Never overwrite the creator's original prompt.

---

## P1 — creative memory

### 5.7 Reference Genome

Restore reusable:

- canon,
- character identity anchors,
- style defaults,
- palettes,
- typography rules,
- composition rules,
- negative/exclusion defaults,
- approved examples,
- training/reference feedback.

### 5.8 StyleStack / StyleDNA

Distinguish:

- prompt keyword style,
- model mode,
- provider preset,
- image reference,
- saved style,
- quick reference,
- custom model,
- portable StyleDNA.

A single `style_expert` string cannot represent this.

---

## P1 — orchestration

### 5.9 Workflow engine

Restore creative workflows such as:

- asset pack,
- character system / character sheet,
- style bible,
- storyboard,
- brand campaign,
- manga/comic page,
- product mockup pack,
- collection manifest export,
- custom-model training pipeline.

The current `pipeline.py` is ingestion orchestration. It should not be confused with creative workflow orchestration.

### 5.10 Provider/model policy router

Model/provider choice should be policy-driven from:

- quality,
- cost,
- latency,
- typography,
- character consistency,
- style consistency,
- batch size,
- resolution,
- provider availability.

The current Ideogram model-capability parser is useful input to this future router.

---

## P2 — evaluation and approval

Add structured evaluations for:

- character consistency,
- style consistency,
- text accuracy,
- layout compliance,
- continuity,
- duplicate/near-duplicate detection,
- quality/readiness.

Evaluation should write explicit data. It should not silently delete/reject assets.

Add human approval/review state so approved outputs can feed Reference Genome or training datasets.

---

## P2 — real asset durability

Current persistence stores metadata and remote URLs. Earlier design explicitly warned that provider URLs must not become the durable system of record.

Still required:

- blob/object store abstraction,
- content hash,
- local/remote durable object locator,
- file size/MIME/dimensions,
- source URL as provenance rather than sole storage,
- asset integrity verification,
- optional mirror/download policies.

---

## P2 — platform state and async jobs

Still missing from the earlier stateful runtime:

- organizations/workspaces,
- datasets,
- custom model records/training jobs,
- generation job/status events,
- queue/worker model,
- retries/backoff/rate-limit metadata,
- partial-failure records,
- webhook/event ingestion.

---

# 6. Smaller gaps discovered during this audit

## Documentation drift

`docs/ROADMAP.md` still marks some already-landed work incomplete:

- optional SQLite FTS5 exists in `fts.py`,
- Ideogram reference collections are already normalized by `adapters/ideogram/references.py`.

This should be corrected immediately.

## Repository map drift

The README repository map predates some later additions such as:

- `dataset_pack.py`,
- `audit.py`,
- `fts.py`,
- `pipeline.py`,
- `references.py`.

## Release hygiene

Still desirable:

- committed `CHANGELOG.md`,
- tagged release/version narrative,
- repository description/topics,
- required CI branch protection rather than merely having a workflow.

## Ideogram DOM enrichment

Userscript captures `feed`, but not currently:

- visible likes,
- visible prompt snippets,
- current model selection,
- visible configuration controls.

Saved-HTML adapter captures identity but not feed/engagement.

## Corpus not yet exercised

The system has not yet been pressure-tested against the accessible full `@avatararts` archive. Synthetic fixtures prove contracts, not corpus-scale completeness.

---

# 7. Non-negotiable invariants recovered from prior work

These should become tests/contracts, not only prose:

1. Never silently substitute edit/remix/reframe/upscale/generate operations.
2. Never claim a provider operation occurred when only mock/local logic ran.
3. Never make provider URLs the durable system of record.
4. Never overwrite the original creator prompt when enhancing it.
5. Never collapse authoring-only references into generation references.
6. Never make Ideogram's JSON shape the provider-neutral canonical format.
7. Never flatten repeated character instances when identity linkage exists.
8. Never turn collection cleanup into permanent asset deletion implicitly.
9. Preserve source IDs and parent/derivative lineage on transformations.
10. Surface partial failures in bulk workflows.
11. Keep provider-specific behavior behind provider backends/dialects.
12. Record verified facts, inferences, and unresolved claims separately.

---

# 8. Recommended merged architecture

Do not throw away the current recovery work and do not resurrect a second disconnected CreativeOS repository.

Merge the two architectural branches:

```text
                         CONTENT UNIVERSE
                              │
         ┌────────────────────┴────────────────────┐
         │                                         │
  EVIDENCE / RECOVERY                       CREATIVE AUTHORING
         │                                         │
 HAR · HTML · CSV · JSON                    Creative Brief
 Browser collectors                         Canon / Character
 Platform archive APIs                      Style / References
         │                                         │
         ▼                                         ▼
 Recovery Adapters                           Prompt Builder
         │                                         │
         └────────────────┐         ┌──────────────┘
                          ▼         ▼
                     CANONICAL GRAPH
          entities · assets · provenance · lineage
                          │
                ┌─────────┴─────────┐
                ▼                   ▼
          CreativeOS Runtime     Reference Genome
                │                   ▲
        Workflow / Router            │
                │                   │
       Provider Backend/Dialect      │
                │                   │
   iDeoMine · Leonardo · FLUX · ... │
                │                   │
                ▼                   │
        Generation / Transform      │
                │                   │
                ▼                   │
        Evaluation / Approval ──────┘
                │
                ▼
       Durable Asset / Content Graph
```

### Important naming distinction

- **Recovery Adapter**: parses existing evidence/history.
- **Provider Backend**: performs supported live operations.
- **Provider Dialect**: translates provider-neutral structured intent into provider semantics.
- **Workflow**: composes authoring, provider operations, evaluation and persistence.

Do not force these into one interface merely because all of them are "platform integrations."

---

# 9. Correct next sequence

## Save point A — documentation parity

- add this audit,
- fix roadmap stale checkboxes,
- add the earlier product boundaries to architecture/handoff,
- commit changelog.

## Save point B — contract recovery

Add provider-neutral contracts first, without live provider calls:

- semantic operation enum/contracts,
- SceneGraph,
- TypographyLayer,
- PromptManifest + PromptLineage,
- StyleStack + StyleDNA,
- Reference Genome,
- provider capability/backend protocols,
- evaluation/approval models.

Test the invariants before adding live transport.

## Save point C — migrate old working runtime concepts

Reconstruct/migrate:

- provider registry,
- mock backend,
- remote MCP backend boundary,
- workflow engine,
- asset-pack workflow,
- character-system workflow,
- style-model training workflow.

Do not rewrite functioning concepts as unrelated new abstractions unless the Content Universe data model actually requires the change.

## Save point D — real corpus pressure test

- crawl/import the accessible `@avatararts` archive,
- reconcile request/response/asset counts,
- run completeness audit,
- batch-enrich missing metadata,
- generate model/style/prompt evolution reports,
- identify lineage/reference ambiguities from real data.

## Save point E — provider-backed authoring

Only after the provider-neutral contracts are stable:

- connect supported Ideogram/first-party MCP or API backend,
- preserve explicit operation semantics,
- persist outputs immediately,
- add retry/rate-limit/cost/privacy state,
- add structured authoring transforms where legitimately supported.

---

# 10. Audit verdict

Content Universe is **not a failed migration**. The new repository successfully solved a part of the earlier design that had been weak: durable recovery, provenance, cross-platform ingestion, normalized identity, SQLite persistence, and an explicit creator graph.

But the migration is **incomplete**.

The repository currently embodies roughly:

```text
CreativeOS / iDeoMine vision
        │
        ├── durable Asset Graph / recovery side  → substantially implemented
        └── structured authoring/runtime side    → mostly not migrated
```

The next expansion should therefore stop asking "what other extractor can we add?" long enough to recover the already-designed authoring/runtime half.

That is the most important thing the chronological review found that the current GitHub repository had missed.
