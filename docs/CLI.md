# CLI Guide

## `content-universe adapters`

List registered source adapters.

```bash
content-universe adapters
```

## `content-universe harvest`

Auto-detect a supported source and normalize it.

```bash
content-universe harvest SOURCE [outputs]
```

Outputs:

```text
--summary
--json path.json
--jsonl path.jsonl
--csv path.csv
--sqlite path.sqlite
--mermaid lineage.mmd
--asset-manifest assets.json
```

Example:

```bash
content-universe harvest ideogram.ai-avatararts.har \
  --summary \
  --sqlite catalogs/avatararts.sqlite \
  --jsonl catalogs/avatararts.jsonl \
  --asset-manifest catalogs/avatararts.assets.json \
  --mermaid catalogs/avatararts.mmd
```

## `content-universe network-inventory`

Build a query-string-free endpoint inventory from a HAR without replaying requests.

```bash
content-universe network-inventory ideogram.ai-all.har --host ideogram.ai
```

Write JSON:

```bash
content-universe network-inventory ideogram.ai-all.har \
  --host ideogram.ai \
  --json research/ideogram-endpoints.json
```

## `content-universe sanitize-har`

Create a conservative redacted candidate fixture.

```bash
content-universe sanitize-har private.har candidate.har
```

For schema-only research:

```bash
content-universe sanitize-har private.har candidate.har --strip-response-bodies
```

**Always manually inspect the result before publication.** The sanitizer cannot know every platform-specific secret field.

## `content-universe prompt-analyze`

Analyze original and expanded/autoprompt content.

Inline:

```bash
content-universe prompt-analyze \
  --original 'make a poster' \
  --expanded '{"high_level_description":"..."}'
```

From a file:

```bash
content-universe prompt-analyze \
  --original 'make a poster' \
  --expanded @expanded-prompt.json
```

## `content-universe models-from-json`

Inspect captured/sanitized Ideogram model catalog JSON.

```bash
content-universe models-from-json model-catalog.json
```

Only models supporting style references:

```bash
content-universe models-from-json model-catalog.json \
  --capability supports_style_reference
```

Only custom models:

```bash
content-universe models-from-json model-catalog.json --custom yes
```

## Output philosophy

CLI outputs are intentionally local and composable. Content Universe does not upload catalogs or captures automatically.
