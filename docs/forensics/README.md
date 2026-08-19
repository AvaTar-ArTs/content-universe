# Canonical Forensic Continuation

This directory is the repository-facing entry point for the **v5 canonical forensic lineage**. It does not replace the earlier savepoint and migration audits; it layers a newer cross-repository continuation model on top of them.

## Start here

1. [`FORENSIC_MASTER_AUDIT_v5.md`](FORENSIC_MASTER_AUDIT_v5.md) — current canonical synthesis.
2. [`SOURCE_AUTHORITY_RULES_v5.md`](SOURCE_AUTHORITY_RULES_v5.md) — which source wins for which question and how conflicts are handled.
3. [`GITHUB_CONVERGENCE_PLAN_v5.md`](GITHUB_CONVERGENCE_PLAN_v5.md) — the recommended bridge sequence across Content Universe, Creator Camp, My Creators, CreativeOS and provider-specialist systems.
4. [`CAPABILITY_MATRIX_v5.csv`](CAPABILITY_MATRIX_v5.csv) — capability ownership/parity across lineages.
5. [`ECOSYSTEM_GAP_REGISTRY_v5.json`](ECOSYSTEM_GAP_REGISTRY_v5.json) — machine-readable unresolved contract/runtime gaps.
6. [`VALIDATION_v5.json`](VALIDATION_v5.json) — validation snapshot for the forensic build.

## Relationship to earlier repository audits

The earlier repository documents remain historically valuable:

- `docs/CONVERSATION_SAVEPOINT_AUDIT.md`
- `docs/CREATIVEOS_MIGRATION_AUDIT.md`
- `docs/ARCHITECTURE.md`
- `docs/RESEARCH_HANDOFF.md`
- `docs/ROADMAP.md`

The v5 forensic layer adds two concepts that should remain explicit going forward:

- **TH checkpoints** preserve exact conversation/request evidence.
- **SP savepoints** preserve architectural conclusions that can span several conversations or code versions.

## Source authority

Current GitHub remains authoritative for current `content-universe` implementation state. Historical CreativeOS/iDeoMine archives remain authoritative for capabilities that existed there but have not migrated. Creator Camp and My Creators keep ownership of their publishing/IP-governance and local-production domains until shared versioned contracts are established.

Inaccessible external evidence is preserved as a locator/status only. Its contents are never guessed.

## Distribution policy

Large forensic master/group ZIP bundles are intentionally **not committed to the repository**. The repository stores the continuation metadata, audits, matrices, schemas and build rules. Release automation can later publish signed/checksummed distribution artifacts without turning Git history into binary storage.
