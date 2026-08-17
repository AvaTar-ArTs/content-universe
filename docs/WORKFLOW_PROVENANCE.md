# Workflow Provenance and Creative Execution

This document defines how agent-skill workflow decisions become durable Content Universe evidence.

The repository does **not** copy skill instructions or become a second agent-skills runtime. `agent-skills` owns behavioral methodology. Content Universe owns durable identity, provenance, execution records, checkpoints, creative artifacts, evaluation, verification, and graph lineage.

## Architecture boundary

```text
user intent
  -> process skill
  -> structured handoff
  -> domain skill
  -> semantic workflow
  -> tool / MCP
  -> provider or local backend
  -> durable asset(s)
  -> evaluation / approval
  -> verification
  -> Content Universe graph
```

The important boundary is between semantic intent and provider execution. Provider names, URLs, transient jobs, and UI actions never replace canonical workflow or artifact identity.

## New durable contracts

### `SkillInvocationRecord`

Records which skill selected or participated in work. It may include skill version, semantic capability, selected workflow, tool/MCP, provider/backend, inputs, outputs, and metadata.

This is provenance, not a replacement for the skill definition itself.

### `WorkflowHandoff`

Carries the durable boundary between skills or workflow stages. It preserves:

- source and destination skill
- selected workflow
- approved design reference when available
- canonical inputs and outputs
- assumptions
- unresolved questions

A handoff prevents downstream agents from reconstructing intent from chat archaeology.

### `WorkflowRun`

Represents one execution of a named semantic workflow. A run can point to:

- skill invocations
- handoffs
- checkpoints
- provider jobs
- verification records
- canonical inputs and outputs
- a parent run when resuming or branching

`WorkflowRun.status=completed` should only be used when the workflow's own completion contract has been satisfied.

### `WorkflowCheckpoint`

A resumable checkpoint records phase, status, completed steps, durable artifacts, unresolved items, and whether continuation is supported.

Checkpoints are first-class graph entities rather than log lines. Partial completion is therefore representable without pretending the whole workflow succeeded.

### `ProviderJobRecord`

A provider job is the durable execution envelope underneath a semantic workflow. It preserves requested operation, executed operation, execution mode, provider, provider-call truthfulness, status, inputs, outputs, warnings, and raw evidence.

Hard invariants:

1. requested and executed semantic operations must match;
2. provider mode requires evidence that a provider call occurred;
3. local or mock execution cannot claim provider execution;
4. a transient provider URL or UI job is not canonical identity.

`ProviderJobRecord.from_operation_result()` converts the existing operation result contract into the durable job representation.

### `VerificationRecord`

Verification is distinct from generation, evaluation, and approval.

A verification record states a concrete claim, status, evidence refs, verifier, and verification type. `PASS` requires at least one durable evidence reference. This deliberately prevents claims such as "published", "persisted", "rendered", or "provider executed" from existing without evidence.

## Audiovisual workflow contracts

The `music-to-video` skill introduced a useful cross-media sequence. Content Universe stores the durable semantic artifacts rather than the skill prose.

### `CueMap`

A cue map links a canonical track to ordered, non-overlapping timeline cues. Each cue can preserve musical/lyrical event, energy, and visual intent.

### `ShotManifest`

A shot manifest is downstream of a cue map and workflow run. Each `ShotSpec` carries:

- shot and scene identity
- cue IDs
- timing
- framing and camera intent
- action, emotion, and location
- optional PromptManifest and SceneGraph links
- typed references
- protected fields
- render requirements

A `SceneGraph` and a `ShotManifest` are intentionally different abstractions. SceneGraph describes semantic scene content. ShotManifest describes executable timeline coverage. One may expand into the other, but neither should overwrite the other.

## Typed reference roles

Existing reference roles remain authoritative:

- `AUTHORING`
- `GENERATION`
- `EVALUATION`
- `CONTINUITY`

A reference can therefore be used to preserve identity without automatically being passed to a generation provider. The shot-manifest graph bridge records the role and reference kind on each relationship.

## Graph vocabulary

New entity kinds:

- `workflow_run`
- `skill_invocation`
- `workflow_handoff`
- `checkpoint`
- `verification`
- `cue_map`
- `shot_manifest`

Existing `workflow` and `provider_job` remain canonical semantic and execution concepts.

New edge kinds:

- `selected_workflow`
- `invoked_as`
- `handed_off_to`
- `checkpoint_of`
- `executed_as`
- `verified_by`
- `cue_map_for`
- `shot_plan_for`
- `resumes`

Repeated shot/reference relationships receive edge IDs so repeated appearances are not flattened by graph deduplication.

## Music-to-video example lineage

```text
TRACK
  <- cue_map_for - CUE_MAP
                    ^
                    | uses
WORKFLOW_RUN -> SHOT_MANIFEST
    |               | uses scene/prompt/reference contracts
    | executed_as   v
    +----------> PROVIDER_JOB -> produced -> ASSET / VIDEO
    |
    +----------> CHECKPOINT
    |
    +----------> VERIFICATION -> uses -> durable evidence
```

A richer end-to-end run may be:

```text
brainstorming
  -> WorkflowHandoff
  -> music-to-video SkillInvocation
  -> WorkflowRun
  -> CueMap
  -> SceneGraph(s)
  -> ShotManifest
  -> PromptManifest(s)
  -> ProviderJob(s)
  -> StructuredDesignAsset / Video
  -> Evaluation
  -> Approval
  -> Verification
```

## Cross-repository authority

- `AvaTar-ArTs/agent-skills` owns skill behavior, routing methodology, and workflow instructions.
- `AvaTar-ArTs/content-universe` owns canonical durable workflow/execution/evidence records and graph identity.
- Provider backends own execution mechanics, never canon.
- Recovery adapters import historical evidence, never impersonate live provider execution.

This boundary keeps the ecosystem composable: skills can evolve without schema duplication, and Content Universe can preserve exactly which skill/workflow/tool/provider path produced an artifact.

## Interchange schemas

Machine-readable interchange is provided for:

- `schemas/workflow-run.schema.json`
- `schemas/shot-manifest.schema.json`

The Python dataclasses are the runtime source of truth. Schemas are interchange contracts for external tools and agents.
