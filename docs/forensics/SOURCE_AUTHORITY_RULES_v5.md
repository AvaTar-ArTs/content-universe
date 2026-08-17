# Source Authority and Conflict Rules v5

The forensic product contains multiple truthful-but-temporally-different sources. This file defines which source answers which question.

## Authority order by question

### Current `content-universe` implementation
1. Current GitHub connector observation of `AvaTar-ArTs/content-universe`
2. Matching current user-provided repository snapshot
3. Prior forensic bundles
4. Historical CreativeOS/iDeoMine archives
5. Conversation intent/specification

### Creator Camp / My Creators implementation
1. Latest user-provided repository snapshots in this build
2. Their own repository docs/tests/templates
3. Cross-repo integration audits
4. Conversation design intent

### Historical capability or rejected design
1. Original archived source edition that contained the capability
2. Contemporary handoff/decision ledger/ontology/spec
3. Later audit interpretation

### Product intent and rationale
1. Exact user conversation/export checkpoint
2. Explicit decision ledger/handoff
3. Architecture docs
4. Implementation inference

### Inaccessible external evidence
Never infer content. Preserve locator + retrieval status only.

## Conflict rules

- Newer code may supersede older implementation without erasing the older rationale.
- A newer README does not supersede executable code when they disagree about what is implemented.
- A historical implementation does not override current security or semantic invariants merely because it once worked.
- Provider/web evidence and recovered HAR schemas remain evidence, not promises of stable external APIs.
- "Missing" means missing from the compared source, not necessarily impossible or never designed.
- "Implemented" means executable code/contract exists in the named lineage, not that every live backend is connected.

## Canonical preservation rule

Every consequential capability is represented as at least one of:
- executable implementation,
- explicit deferred item,
- documented historical implementation,
- rejected/superseded design with reason, or
- unresolved evidence locator.

No important concept should exist only in transient chat memory.
