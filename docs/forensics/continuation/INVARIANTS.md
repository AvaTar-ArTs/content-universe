# Non-Negotiable Invariants

These are architectural tests waiting to happen.

1. Never silently substitute `generate`, `edit`, `remix`, `reframe`, `upscale`, or other semantic operations.
2. Never claim a provider operation occurred when execution was mock/local.
3. Never overwrite the original creator prompt.
4. Never collapse authoring references into generation-conditioning references.
5. Never use Ideogram's provider JSON as the provider-neutral canonical schema.
6. Never collapse repeated entity instances merely because source/target IDs match.
7. Never assume deleting a collection means deleting its contained assets.
8. Never lose parent/source IDs during transforms.
9. Never hide partial failures in bulk/workflow execution.
10. Never treat provider URLs as the sole durable asset location.
11. Never place provider authentication secrets into fixtures, logs, handoffs or public HARs.
12. Never mix recovery adapter responsibilities with live provider mutation responsibilities.
13. Never treat an infrastructure MCP as proof of a creative provider integration.
14. Never conflate request/operation counts with response/output counts or asset counts.
15. Never treat absence of evidence as evidence of absence in historical reconstruction.
16. Never let a UI or canvas become the system of record when portable structured state can represent it.
17. Never make a provider-specific knob mandatory in cross-provider objects unless it has portable meaning.
18. Never mark an integration production-ready solely because a README describes it.
19. Never discard raw provider payloads before canonical normalization is proven complete.
20. Never let newer docs silently erase the historical checkpoint they supersede.
