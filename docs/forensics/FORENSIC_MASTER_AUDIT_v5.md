# Content Universe / CreativeOS Canonical Forensic Master Audit v5

**Date:** 2026-08-17  
**Compared GitHub:** `AvaTar-ArTs/content-universe`  
**Observed GitHub head:** `a07928fda9dc6e729c3359f53f1c4d01adefad73`  
**Method:** exact thread checkpoints + architectural savepoints + historical source artifacts + current source snapshots + executable validation + source-authority rules.

## Executive verdict

The ecosystem is no longer best described as one repository or even two products. The recovered architecture has four cooperating operational planes plus provider-specialist subsystems:

```text
Creator Camp
canon · rights · serialization · publishing · adaptation · release governance
        ↓
CreativeOS
structured authoring · semantic operations · workflows · routing · evaluation
        ↓
My Creators / provider backends
local production · training · ShotManifest · RenderPlan · ComfyUI / other execution
        ↓
Content Universe
identity · provenance · lineage · graph · durable catalog · reusable memory

Specialists: iDeoMine (Ideogram-native), Suno subsystem, future provider plugins
```

These planes should share IDs/contracts and one durable truth substrate, but they should not be flattened into one giant source folder.

## Dual memory model

The canonical product now maintains two independent histories:

- **TH checkpoints** preserve exact conversation/request evidence.
- **SP savepoints** preserve architectural conclusions that may span several conversations and code versions.

This matters because one sentence in a later audit can summarize weeks of decisions but cannot replace the exact prompt/branch that produced them.

### New v5 checkpoints

- **TH-14** — canonical rebuild mandate: start at the beginning, compare continuously, preserve memory, compare GitHub, emit master + independent groups.
- **TH-15** — shared ChatGPT conversation locator. Body unavailable through public fetch path, therefore recorded as unresolved evidence without invented summary.
- **SP-24** — canonical forensic packaging protocol.
- **SP-25** — unresolved external evidence protocol.
- **SP-26** — stable GitHub head during v5.
- **SP-27** — source-authority/conflict rules.

## What the conversation lineage taught in order

### 1. Suno was the extraction genome
The mature pattern was discovery before enrichment, canonical ID maps, adaptive scrolling, retry/concurrency thinking, offline recovery, intelligent richer-row merges, and exports that rebuild a master catalog. Current GitHub inherited the recovery philosophy but still lacks a generic resumable enrichment worker runtime.

### 2. iDeoMine was never meant to be only image generation
Generate, edit, remix, reframe, upscale, describe, collections, history, datasets, training/models and organization state were treated as distinct provider semantics. Current GitHub now restores typed semantic operations and provider contracts but still lacks broad live provider transport/state execution.

### 3. CreativeOS separated intent from providers
Prompt Builder, SceneGraph, PromptLineage, StyleDNA, Reference Genome, provider routing, workflows, evaluation and many interfaces were designed as one headless runtime. GitHub has recovered much of the contract layer, but v2/market remain stronger references for provider breadth, federation and older interface/workflow experiments.

### 4. Ideogram evidence made recovery concrete
HARs and saved DOM showed request/response/asset identity, structured autoprompts, models, seeds, dimensions, reference collections, profile pagination and lineage clues. GitHub is the strongest executable recovery implementation.

### 5. Content Universe solved durable memory
The new repository made identity/provenance/SQLite/graph/recovery cross-platform. The later CreativeOS migration correctly reused that substrate instead of reviving a second state store.

### 6. Entity instances forced the graph to mature
The system learned that relationship type is not enough when the same character appears twice in one scene. `edge_id` and the SQLite migration preserve relationship instances as well as relationship semantics.

### 7. Creator Camp added IP/release governance
Canon, public/commercial editions, rights, serialization, submission, adaptation and release evidence are not merely metadata. They form a governance plane that should persist through Content Universe but remain owned by publishing/IP workflows.

### 8. My Creators added concrete local execution
Shot manifests, RenderPlans, local backend constraints, training plans, component registries and license discipline supply the production plane CreativeOS contracts were previously missing.

### 9. v5 makes forensic continuation itself a product contract
The repeated user instruction requires not only complete archives but a reproducible memory system. Inaccessible evidence must remain visible without becoming fabricated evidence.

## Current implementation comparison

### GitHub `content-universe`
Best current source for:
- recovery adapters,
- canonical identity/provenance,
- graph + SQLite/query,
- typed current CreativeOS contracts,
- Prompt Builder local runtime,
- provider abstractions,
- Ideogram provider catalog,
- StructuredDesignAsset and instance-aware graph persistence.

### CreativeOS Everything v2
Still valuable for:
- provider categories/roles,
- evidence/trust registry,
- broad provider catalog,
- cross-media identity/operation/job/cost/workflow models,
- Action MCP/router scaffolds,
- comprehensive use-case/workflow catalog,
- Suno multi-backend strategy.

### CreativeOS v0.3.1 Market
Still valuable for:
- old remote MCP federation implementation,
- provider-control TUI,
- earlier workflow engine,
- ReferenceLibrary,
- Prompt Builder docs/fixtures and interface history.

### Creator Camp
Canonical adjacent owner for:
- canon/edition separation,
- rights/adaptation records,
- serialization/submission/release workflows,
- IP governance and release evidence.

### My Creators
Canonical adjacent owner for:
- local production bootstrapping,
- ShotManifest/RenderPlan,
- ComfyUI workflow seam,
- style/character/environment adapter training,
- component registry and license discipline.

## Most important unresolved merge work

1. Versioned shared contract package across all repos.
2. `RightsRecord`, `EditionRecord`, `ReleaseRecord`, `LicenseManifest`.
3. `SceneContract → SceneGraph → ShotManifest → RenderPlan` bridge.
4. `ProviderJob` + `RenderCheckpoint` + retries/partial failures/cost/latency.
5. My Creators backend implementing CreativeOS `ProviderBackend`.
6. Action MCP/workflow runtime over current semantic contracts.
7. Provider evidence/trust/role/category registry.
8. Durable content-addressed media/object store.
9. Real full `@avatararts` Ideogram corpus pressure test.
10. Runtime `EvidenceStatus` / unresolved-source model.
11. Source-to-claim provenance graph.
12. CI-native signed canonical forensic release packaging.

## Non-negotiable invariants

1. Never silently substitute generate/edit/remix/reframe/upscale.
2. Never claim live provider execution from mock/local-only behavior.
3. Never make remote provider URLs the durable asset identity.
4. Never overwrite original creator prompts.
5. Never collapse authoring vs generation references.
6. Never make provider JSON the cross-provider canonical schema.
7. Never flatten repeated identity-linked instances.
8. Never imply collection cleanup deletes source assets.
9. Preserve transformation parent/source IDs.
10. Surface partial failures.
11. Keep provider-specific semantics behind backends/dialects.
12. Distinguish verified evidence, inference, rejected ideas and unresolved claims.
13. Infrastructure MCPs are not automatically creative providers.
14. Keep request/response/asset counts independent.
15. Browser collectors do not own/exfiltrate auth/session secrets.
16. Inaccessible sources remain unresolved, not guessed.
17. A standalone product group must carry enough memory to continue independently.

## Final architecture

```text
                       CONTENT UNIVERSE
                  memory · evidence · graph
                           ▲       ▲
                           │       │
              evaluation/approval │ release evidence
                           │       │
                     CREATIVEOS    │
          authoring · workflow · routing · jobs
              ▲             ▲             ▲
              │             │             │
         iDeoMine       My Creators      Suno / others
       Ideogram-native   local render     provider plugins
              ▲             ▲
              └──────┬──────┘
                     │
               Creator Camp
       canon · rights · release · adaptation
```

The shared object is not a mega-repository. The shared object is the **versioned contract + durable graph**.

## v5 validation

- Current Content Universe supplied snapshot: **39 tests passed**.
- My Creators supplied snapshot: **5 tests passed**.
- Creator Camp local Markdown link audit: **0 broken relative links**.
- Current GitHub main observed unchanged at `a07928f…`.
- Shared ChatGPT URL retained as unresolved evidence because body was not fetchable.
- Raw authenticated HAR/cookie/session material excluded from public forensic bundles.

## Packaging verdict

v5 is the canonical continuation edition. It preserves all prior v4 lineages plus the current packaging mandate and unresolved external-source protocol. The master is the complete organism; the grouped product is the set of independently usable organs.
