# CreativeOS Migration Audit

**Audit date:** 2026-08-17  
**Compared systems:** archived iDeoMine / CreativeOS v0.3.x design and source evidence, pre-audit Content Universe v0.3, and the merged Content Universe + CreativeOS contract layer created during this review.

This document answers a narrower question than the chronological save-point audit:

> Which old CreativeOS ideas should be restored, which current Content Universe ideas are stronger, which historical implementation choices should be discarded, and what is still genuinely missing?

---

## Executive verdict

The strongest system is not the old CreativeOS package by itself and not the recovery-focused Content Universe by itself.

The stronger architecture is the merge:

```text
Content Universe
  = durable identity + recovery + provenance + graph + persistence

CreativeOS
  = portable authoring + semantic operations + provider contracts + evaluation

iDeoMine
  = Ideogram-native capability/state depth behind provider boundaries
```

The old system had richer **creative semantics**. The new repository had much stronger **durable evidence/recovery architecture**. The current migration combines them while removing several historical weaknesses.

---

## Comparison matrix

| Area | Archived CreativeOS / iDeoMine | Content Universe before this audit | Merged state after this audit | Verdict |
|---|---|---|---|---|
| Identity/provenance | planned provenance and manifests | strong canonical IDs, provenance ledger, graph | reused as durable substrate | keep current |
| Recovery from HAR/HTML/CSV/JSON | not the central strength | strong multi-source adapters | unchanged | keep current |
| Suno richer-row recovery | historical precursor | generalized completeness merge | unchanged | keep current |
| Semantic image operations | explicit generate/edit/remix/reframe/upscale | absent as execution contracts | typed `OperationKind` + validators | restore/improve |
| No silent substitution | prose/server checks | lineage only | executable request/result invariant | improve |
| Original prompt preservation | explicit design invariant | original/expanded recovery data | immutable `PromptLineage` | improve |
| Reference roles | authoring/generation/evaluation/continuity | generic references/edges | typed `ReferenceBinding` roles | restore/improve |
| `passed_to_generation` | separate field in Prompt Builder spec | absent | derived from role, avoiding contradictory state | improve old design |
| Prompt Builder | local structured-authoring runtime | only prompt decomposition | local runtime restored | restore |
| Provider-backed Prompt Builder methods | intentionally not simulated | absent | explicit `ProviderOperationRequired` boundary | restore/improve |
| Ideogram JSON | import/export dialect | captured structured prompt parsing | reversible dialect using observed fields | restore + connect evidence |
| SceneGraph | typed authoring model | structured prompt decomposition only | typed `SceneGraph`/elements/bounds | restore |
| TypographyLayer | typed shell/Layerize target | raw text element fields | typed layer | restore |
| Entity vs instance | CharacterEntity -> ObjectInstance[] | generic entities only | SceneElement instance IDs + canonical `entity_ref` + graph `INSTANCE_OF` | restore with simpler model |
| Repeated slogan/concept identity | planned | absent | reusable `concept` entities | restore |
| StyleStack | multiple simultaneous mechanisms | provider style fields/raw metadata | ordered typed stack | restore |
| StyleDNA | portable style abstraction | absent | typed `StyleDNA` | restore |
| Reference Genome | implemented/planned memory layer | absent | typed genome + durable bridge | restore |
| StructuredDesignAsset | canonical ontology item | absent | typed design object + masks/windows/lineage | restore |
| Evaluation/approval | evaluation roadmap | absent | durable record contracts and graph edges | restore baseline |
| Provider registry | implemented | recovery adapter registry only | separate execution registry | restore without conflation |
| Provider capabilities | provider runtime feature | Ideogram model capability parser only | generic execution capability contract + provider-native recovery evidence | merge |
| Provider dialect | explicit idea | absent | separate protocol from backend | restore |
| Mock backend | existed but random UUID IDs despite deterministic wording | absent | deterministic semantic-request hash | replace old implementation |
| Provider tool catalog | 26 iDeoMine tools | absent from execution layer | declarative 26-tool Ideogram catalog | restore as metadata/contracts |
| Backend API | `call(tool: str, arguments: dict)` | no live backend | typed semantic `execute(OperationRequest)` | reject old stringly design |
| Remote MCP federation | implemented in old package | absent | still missing | revisit after async policy/current SDK verification |
| Workflow engine | direct string provider calls | recovery `pipeline.py` only | still missing | redesign, do not copy blindly |
| TUI | provider control deck | query TUI | query TUI remains; creative views missing | merge later |
| MCP | semantic provider/workflow MCP | query MCP | semantic MCP still missing | merge later |
| Durable blob storage | missing | metadata/URL persistence | still missing | high priority |
| Worker/webhook/job system | missing | absent | absent | high priority after contracts |
| Full real-corpus testing | provider-oriented fixtures | mostly synthetic recovery fixtures | still needs full archive pressure test | high priority |

---

## Improvements over the historical implementation

### 1. Typed semantic operations instead of stringly provider calls

Historical workflows called provider tools by strings such as:

```text
backend.call("create_collection", {...})
backend.call("generate_images_bulk", {...})
```

That was a useful scaffold, but it let provider vocabulary leak directly into orchestration.

The merged design separates:

```text
OperationRequest          provider-neutral intent
ProviderDialect           structured translation
ProviderBackend           live/mock execution
ProviderToolCatalog       provider-native state/capability inventory
Recovery Adapter          evidence/history parser
```

A workflow can therefore reason in semantic operations while still accessing provider-native state where necessary.

### 2. Deterministic mock means deterministic

The archived handoff itself noted that the old mock generated random UUID fragments despite documentation describing it as deterministic.

The new `DeterministicMockBackend` hashes the normalized semantic request, producing stable job/output IDs for the same request.

It also cannot claim a provider call happened:

```text
execution_mode = mock
provider_call_performed = false
```

### 3. Reference generation intent cannot contradict itself

The older Prompt Builder spec wanted both semantic role and a `passed_to_generation` flag.

Maintaining both as writable fields allows impossible state:

```text
role = authoring
passed_to_generation = true
```

The new contract derives `passed_to_generation` from `ReferenceRole.GENERATION`.

### 4. Entity-instance identity without redundant class forests

The archived ontology used conceptual subclasses such as ObjectInstance and TextInstance.

The merged design keeps one typed `SceneElement` instance model:

```text
element_id       = this appearance
kind             = object/text/etc
entity_ref       = reusable Character/Concept/etc identity
```

Two scene elements can therefore point to the same character while retaining separate geometry and metadata.

Persistence emits `INSTANCE_OF` graph relationships with the element ID attached.

### 5. Provider-backed authoring methods fail explicitly

`describe`, `magic_prompt`, `layerize_text`, and provider-backed `edit` do not produce invented local results.

They construct the semantic `OperationRequest` and raise `ProviderOperationRequired` until a real backend is supplied.

This makes the historical non-simulation rule executable.

### 6. StructuredDesignAsset now sits on the durable graph

The old ontology correctly recognized that a finished creative object is more than a raster.

The new contract can bind:

```text
StructuredDesignAsset
├── base asset
├── SceneGraph
├── PromptManifest
├── StyleDNA[]
├── vector assets
├── masks
├── generation windows
└── parent StructuredDesignAsset
```

Graph persistence records these dependencies and derivative lineage.

---

## Important things deliberately not ported yet

### Remote MCP backend

The archived implementation used an async MCP client while the new provider protocol is currently synchronous.

Do not paste the old class into the new package. First decide the runtime policy:

- synchronous core + async adapter wrapper,
- async-first provider runtime,
- or explicit sync and async backend protocols.

Then verify the current MCP SDK before implementation.

### Old workflow engine

The old workflows are valuable product ideas:

- asset pack,
- character system,
- style model training.

But the implementation called provider tool strings directly. Rebuild them against typed semantic operations and explicit provider-state services rather than copying the orchestration code wholesale.

### Full Ideogram provider-native structured authoring

The current `IdeogramJsonDialect` round-trips only fields established by captured structured prompts:

- `high_level_description`,
- `compositional_deconstruction.background`,
- `elements[].type`,
- `elements[].text`,
- `elements[].desc`,
- preserved unknown element fields.

It does not claim complete parity with every current Ideogram 4.0 JSON prompt/control field.

### Evaluator implementations

Evaluation and approval are now data contracts. Actual character/style/text/layout/continuity evaluators remain future work.

---

## Remaining architectural gaps ranked by impact

### P0 — durable assets

Provider URLs remain observations rather than a true durable asset store.

Needed:

- content hashes,
- blob/object abstraction,
- stable local/object locators,
- integrity verification,
- MIME/size/dimensions,
- optional mirroring policy.

### P0 — workflow engine v2

Build a workflow registry over semantic operations and provider-state services.

First workflows:

1. asset pack,
2. character system/sheet,
3. style bible,
4. storyboard,
5. brand campaign,
6. model-training pipeline.

### P0 — real corpus pressure test

Run the accessible `@avatararts` archive through recovery + CreativeOS import pathways.

Measure:

- request/response/asset counts,
- incomplete records,
- prompt structure frequency,
- model evolution,
- reference collection use,
- lineage ambiguity,
- reusable character/style/concept candidates.

### P1 — continuity

Add continuity constraints and evaluation state on top of entity-instance linkage.

Examples:

- character identity must match approved genome,
- slogan text must be exact across localized variants,
- style DNA must remain within tolerance,
- locked elements must survive a targeted generation window.

### P1 — provider routing

Add policy-driven selection based on:

- operation support,
- model capability,
- cost,
- latency,
- typography,
- style consistency,
- character consistency,
- resolution,
- batch size.

### P1 — interfaces

Expose the restored semantics through MCP/TUI/CLI only after the contracts stabilize.

The current query MCP/TUI should remain intact rather than being replaced.

---

## Recommended next implementation checkpoint

```text
Workflow Engine v2
      │
      ├── WorkflowDefinition
      ├── WorkflowStep
      ├── semantic OperationRequest
      ├── provider-state action
      ├── partial-failure record
      ├── persisted Workflow / ProviderJob entities
      └── emitted StructuredDesignAsset / lineage
```

Start with `create_asset_pack` because it is the smallest historical workflow and exercises:

- collection/project destination,
- prompt manifests,
- provider routing,
- bulk execution,
- partial failure,
- durable output ingestion.

Then rebuild `create_character_system` using Reference Genome and entity-instance continuity rather than simple prompt variants.

---

## Bottom line

The migration should not be framed as “bring the old CreativeOS repo back.”

The useful operation is **selective recombination**:

```text
old CreativeOS semantics
        +
current Content Universe durability/recovery
        -
old stringly provider coupling
        -
false determinism
        -
parallel/disconnected state
        =
merged creative runtime with evidence-backed memory
```

That merged system is now materially closer to the original product thesis than either branch was on its own.
