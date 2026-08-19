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

## `content-universe batch`

Harvest explicit source paths into one merged Content Universe.

```bash
content-universe batch capture-1.har export.json songs.csv --summary
```

Use `--ignore-unsupported` when a manually supplied list can contain files that no adapter recognizes.

## `content-universe analyze-folder`

Bulk-discover and analyze every source in a folder that a registered adapter recognizes. Discovery is adapter-driven, so new adapters automatically participate without maintaining a hard-coded extension list.

```bash
content-universe analyze-folder ~/Downloads/creative-exports --summary
```

By default the command walks subdirectories recursively and skips common dependency/build folders such as `.git`, `node_modules`, `.venv`, `dist`, and `build`.

Useful controls:

```text
--no-recursive                 only inspect direct child files
--include '*.json'             include glob; may be repeated
--exclude '*-private.*'        exclude glob; may be repeated
--max-files 5000               cap candidate files inspected
--strict                       return exit code 2 if unsupported files are found
--discovery-json scan.json     write supported/unsupported/skipped file inventory
```

All normal universe outputs are available, so a directory can be turned into several durable products in one pass:

```bash
content-universe analyze-folder ~/Downloads/creative-exports \
  --include '*.json' \
  --include '*.html' \
  --include '*.csv' \
  --include '*.har' \
  --exclude '*private*' \
  --discovery-json catalogs/discovery.json \
  --sqlite catalogs/content-universe.sqlite \
  --universe-json catalogs/content-universe.json \
  --jsonl catalogs/generations.jsonl \
  --asset-manifest catalogs/assets.json \
  --mermaid catalogs/lineage.mmd \
  --pack catalogs/content-universe.zip \
  --summary
```

Unsupported files are recorded by discovery and ignored by default. `--strict` changes that behavior into a validation gate. Supported files are still harvested through the same adapter registry and normalization pipeline as `harvest` and `batch`.

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
