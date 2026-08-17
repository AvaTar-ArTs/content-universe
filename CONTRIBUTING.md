# Contributing

Content Universe favors evidence-backed adapters over brittle one-off scrapers.

## Adapter checklist

A platform adapter should:

- identify stable platform-native IDs before flattening metadata
- preserve original raw fields where practical
- separate discovery from enrichment
- attach provenance to normalized entities
- emit graph edges only when the source actually supports the relationship
- avoid embedding authentication material
- include sanitized or synthetic regression fixtures
- degrade gracefully when optional fields disappear

## Development

```bash
python -m pip install -e '.[dev]'
ruff check src tests
pytest -q
python -m compileall -q src
```

## Pull requests

Prefer focused commits. For parser changes, include the source shape that motivated the change in the PR description, but never paste secrets or raw authenticated captures.

When adding fields, ask whether the field belongs to:

1. the cross-platform canonical model,
2. platform-specific `raw` metadata,
3. provenance,
4. a graph relationship,
5. an asset/collection entity.

Avoid inflating the canonical model with every platform-specific property.

## Fixture policy

Fixtures must be synthetic or explicitly sanitized. Never commit full production HARs, cookies, bearer tokens, private account exports, or private creative assets.
