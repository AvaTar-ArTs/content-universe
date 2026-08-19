# Polyglot CreativeOS Foundation

Content Universe is intentionally polyglot. Python remains the recovery and AI-worker layer; the public contracts are language-neutral and the surrounding runtime can be implemented in TypeScript, Rust, Go, Swift, SQL, and browser technologies.

## Contract-first rule

All durable interoperability starts with `schemas/creativeos/*.schema.json`. Implementations must preserve:

- stable IDs and provenance
- prompt intent separately from provider expansion
- scene graph geometry in neutral coordinates
- workflow edges and semantic operations
- explicit execution status: observed, modeled, available, executed, verified, or blocked

## Runtime map

| Layer | Technology | Responsibility |
|---|---|---|
| Authoring UI | React + TypeScript | Prompt Builder, scene graph, workflow editor |
| MCP/API adapters | TypeScript | Tool discovery, provider-neutral commands, browser integrations |
| Fast local services | Rust | file indexing, media inspection, deterministic validation |
| Service APIs | Go | stateless HTTP services, queues, health endpoints |
| Apple clients | Swift/SwiftUI | capture, review, local creator companion |
| AI/research workers | Python | vision, embeddings, model calls, recovery adapters |
| Durable data | PostgreSQL + JSONB | entities, lineage, provenance, workflow state |
| Publishing | Astro/Next/MDX | documentation, portfolio, marketplace surfaces |

## Directories

- `packages/creativeos-contracts`: TypeScript types and validators
- `apps/prompt-builder`: browser authoring starter
- `services/indexer-rs`: Rust service boundary
- `services/gateway-go`: Go HTTP boundary
- `clients/CreativeOSKit`: Swift package boundary
- `infra/postgres`: relational substrate
- `workflows`: declarative orchestration examples

## Local verification

```bash
python -m pytest
node --check packages/creativeos-contracts/src/index.mjs
cargo check --manifest-path services/indexer-rs/Cargo.toml
go test ./services/gateway-go/...
```

The starter services are deliberately dependency-light. They establish boundaries that can later connect to the existing Python catalog and MCP server.
