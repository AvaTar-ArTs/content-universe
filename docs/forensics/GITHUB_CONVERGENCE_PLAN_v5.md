# GitHub + Creator Ecosystem Convergence Plan v5

## Principle

**Merge contracts before repositories.** The target is one nervous system, not one giant folder.

## Savepoint 1 — shared contract package

Create/importable versioned contracts for:
- global EntityRef/IDs,
- RightsRecord, LicenseManifest, EditionRecord, ReleaseRecord,
- SceneContract, ShotManifest, RenderPlan bridge types,
- ProviderJob, RenderCheckpoint, CostSnapshot,
- EvidenceStatus / ProviderEvidence / source authority metadata.

Every contract gets Python models + JSON Schema + semantic-versioned identifiers.

## Savepoint 2 — Creator Camp bridge

Import/export:
- rights/provenance registers,
- submission/release trackers,
- canon/edition metadata,
- scene contracts,
- adaptation package metadata.

Persist them through Content Universe graph/storage while Creator Camp keeps workflow/governance ownership.

## Savepoint 3 — My Creators provider plugin

- adapt DryRunBackend to CreativeOS ProviderBackend,
- map SceneGraph/PromptManifest → ShotManifest → RenderPlan,
- persist ProviderJob + RenderCheckpoint,
- add ComfyUI backend,
- gate production by LicenseManifest.

## Savepoint 4 — Action MCP / Workflow Engine v2

Keep current Memory MCP. Add an Action MCP over typed operations/workflows/jobs. Restore the useful federation concepts from v0.3.1 and the router/evidence ideas from v2 without reviving stringly provider calls.

## Savepoint 5 — first full vertical workflow

```text
Creator Camp SceneContract
→ CreativeOS Prompt Builder
→ SceneGraph
→ My Creators ShotManifest / RenderPlan
→ DryRun or ComfyUI ProviderBackend
→ StructuredDesignAsset
→ Evaluation / Approval
→ Creator Camp Edition / ReleaseRecord
→ Content Universe persistence + provenance
```

## Savepoint 6 — provider/evidence registry

Port provider category/role/evidence/trust concepts from v2. Keep creative providers separate from infrastructure MCPs. Route by quality/cost/latency/typography/identity/style/privacy/locality/capability.

## Savepoint 7 — durable media

Add content-addressed object/blob storage, hashes, MIME/dimensions, integrity checks and mirror policy. Provider URLs remain provenance.

## Savepoint 8 — real-corpus pressure test

Run the accessible `@avatararts` Ideogram archive and record request/response/asset counts, malformed structured prompts, unresolved lineage, model/style distribution, merge collisions and asset failures.

## Savepoint 9 — forensic release automation

Move v5 packaging rules into CI/release tooling:
- source snapshot manifest,
- TH/SP ledgers,
- capability/gap matrices,
- security scan,
- checksums,
- master + groups archives,
- signed release/tag.

## Do not do

- do not copy v2/market wholesale over current GitHub,
- do not physically merge Creator Camp/My Creators before contracts stabilize,
- do not collapse recovery adapters and live provider backends into one interface,
- do not use unseen external chats as evidence,
- do not make new provider features bypass provenance/lineage/jobs.
