# Ideogram Evidence Ledger

This document records architecture decisions grounded in captured Ideogram browser evidence supplied during development. Raw authenticated captures are intentionally excluded from the repository.

## Confirmed surfaces

- Public profile information endpoint for a display handle.
- Cursor-paginated profile generation feed at `/api/g/u/profile/c` using `display_handle`, `sort_filter`, and an opaque `cursor`.
- Model catalog endpoint exposing model capability flags.
- Available-resolution metadata.
- Color palette retrieval.
- Request cost/statistics endpoints.
- Canvas listing.
- Batch response metadata retrieval.
- Category and Explore feeds.
- Generation cards with stable semantic `data-testid` identities.
- Generation URLs shaped as `/g/<generation-id>/<response-index>`.
- Response asset URLs containing `/response/<response-id>@<resolution>`.

## Generation metadata observed

Captured records include combinations of:

- `request_id`, `request_type`
- `user_prompt`, `user_negative_prompt`, `caption`
- `responses[].response_id`, `response_index`, prompt, likes, format, visibility
- seed, model version and model URI
- dimensions, aspect ratio, resolution tier
- rendering/sampling speed
- style metadata
- edit/upload/reference parent metadata
- style/character/product reference collection IDs
- completion and error state

## Structured autoprompt evidence

Some Ideogram responses expand a natural-language prompt into a structured composition containing a high-level description, background description, and typed element entries for objects and text. Content Universe should preserve both the original user prompt and the expanded response prompt rather than flattening one into the other.

## Profile archive implication

The profile feed is preferred over infinite DOM scrolling for archive recovery because it returns structured generation records and supports cursor traversal. DOM harvesting remains valuable for passive discovery, regression checks, and recovery when APIs change.

## Explicit non-goals

- Do not commit cookies, bearer tokens, Turnstile tokens, or authenticated request headers.
- Do not hard-code private session material.
- Do not assume undocumented endpoints are stable contracts.
- Do not make raw HARs part of public test fixtures.
