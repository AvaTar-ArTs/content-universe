# Browser Collectors

Browser collectors are intentionally thin field tools. They discover identities and visible evidence while the user browses; they are not the canonical database and they do not own authentication.

## Ideogram userscript

`ideogram-harvester.user.js` watches generation cards using semantic attributes observed in captured Ideogram HTML.

It extracts:

```text
generation_id
response_id
response_index
generation_url
asset_url
asset_resolution
feed
observed_at
source
```

### Why this is separate from HAR/API ingestion

The browser DOM is useful when:

- the API changes
- a gallery has not yet been exported
- the user wants lightweight passive discovery
- an ID appears visually before deeper metadata is fetched

But structured profile/API data is richer and less brittle. Content Universe therefore merges browser observations into canonical records rather than treating DOM output as authoritative.

### Installation

Use a userscript manager such as Tampermonkey/Violentmonkey and install the source file manually from this repository.

### Export

The floating `Content Universe` panel can:

- scan visible cards
- copy collected JSON
- download collected JSON

The collected JSON is suitable for a future dedicated browser-export adapter. Until then, saved HTML and HAR paths remain the richer recovery mechanisms.

## Extension direction

A future browser extension can add capabilities inappropriate for a userscript:

```text
DevTools/network observation
persistent IndexedDB queue
asset manifests
one-click Content Universe export
capture session summaries
bridge to a local Content Universe service
```

The extension should still feed the same canonical adapter/core contracts.

## Security

Do not export browser cookies, authorization headers, or session tokens as part of collector data. Network capture that contains authenticated headers belongs in local HAR files and should be sanitized before sharing.
