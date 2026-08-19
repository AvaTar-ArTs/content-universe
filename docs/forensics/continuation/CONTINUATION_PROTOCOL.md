# Continuation Protocol

## Before doing new work

1. Read `MASTER_HANDOFF.md`.
2. Read relevant save checkpoints.
3. Inspect current GitHub HEAD.
4. Compare HEAD against the checkpoint's recorded status.
5. Search for existing code before creating a parallel implementation.
6. Decide whether the new change belongs to:
   - recovery,
   - canonical graph,
   - authoring,
   - runtime,
   - provider dialect,
   - provider backend,
   - workflow,
   - interface,
   - evidence/research.
7. State which prior checkpoint the change extends or supersedes.

## Before claiming completion

Verify:
- tests,
- compile/lint,
- schema compatibility,
- semantic operation invariants,
- graph lineage,
- provenance,
- security exclusions,
- docs/checkpoint update.

## When adding a provider

Do not begin with code.

First record:
- official/community status
- transport
- auth
- media categories
- semantic operations
- async model
- history support
- asset URL durability
- model discovery
- cost/quota behavior
- local/cloud
- evidence status
- integration priority

Then choose:
- direct backend
- compatibility backend
- reference-only architecture
- recovery adapter
- infrastructure dependency
- no integration.

## When adding a workflow

Workflow code must not call provider tool names directly.

Use:
- semantic operations,
- provider-state service where necessary,
- provider registry/routing,
- explicit jobs,
- explicit partial failures,
- durable output ingestion.

## When changing canonical models

Preserve backward import from provider recovery DTOs.

Never migrate by discarding raw provider evidence.

## When a design changes

Update the save-point ledger.

Use one of:
- preserves
- extends
- supersedes
- rejects

and explain why.
