# Ready-to-Use Continuation Prompt

You are continuing the CreativeOS + Content Universe project.

Before changing code:

1. Read `docs/forensics/README.md`.
2. Read `docs/forensics/SOURCE_AUTHORITY_RULES_v5.md`.
3. Read `docs/forensics/continuation/CONTINUATION_PROTOCOL.md`.
4. Read the save checkpoints relevant to your task.
5. Inspect the current `AvaTar-ArTs/content-universe` HEAD and compare it with the handoff/checkpoints.
6. Prefer extending current GitHub implementations over recreating historical package code.

Architecture:

- Content Universe = durable recovery/evidence/provenance/graph/persistence/query substrate.
- CreativeOS = portable authoring, semantic operations, provider contracts, workflows and evaluation.
- iDeoMine = deep Ideogram-native capability/state layer.
- Suno subsystem = multi-backend audio integration plus historical recovery.
- Reference Genome = approved reusable creative knowledge.

Non-negotiable rules:

- Do not silently substitute semantic operations.
- Do not claim provider execution in mock/local mode.
- Do not overwrite original creator prompts.
- Do not collapse authoring and generation references.
- Do not make provider-specific JSON the canonical cross-provider schema.
- Do not collapse repeated entity instances.
- Do not use provider URLs as durable storage.
- Do not leak auth/session data from HAR/browser captures.
- Do not make recovery adapters perform live provider mutations.
- Surface partial failures.

Current highest-priority implementation target remains the shared contract/workflow bridge described in the forensic convergence plan, followed by durable asset storage, real corpus pressure testing and live provider runtime.

For every meaningful change, update the relevant architectural checkpoint so future agents do not have to reconstruct the reasoning again.
