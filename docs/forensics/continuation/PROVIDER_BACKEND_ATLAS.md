# Provider / Backend Atlas

## Provider classes

### Deep provider
Owns provider-specific semantics and state.
Examples: iDeoMine for Ideogram.

### Official provider MCP/API
Preferred production execution boundary where available.

### Community/reference MCP
May teach architecture or provide optional compatibility. Must not automatically become a dependency.

### Model fabric
Routes across many models/providers.
Examples: fal, Replicate, KIE, Krea-style fabrics.

### Local workflow engine
Runs user-controlled local workflows.
Examples: ComfyUI, Blender, REAPER.

### Infrastructure MCP
Enables browser/system interaction but is not a creative provider.
Examples: Playwright MCP, Chrome DevTools MCP.

### Archive/recovery backend
Reads old captures/exports and reconstructs history.
Examples: Suno extractor lineage, Ideogram HAR/profile adapters.

## Suno backend families

```text
Suno semantic adapter
├── browser/CDP
├── browser/Playwright recon
├── API relay
├── API wrapper
└── archive/recovery
```

References researched:
- unforced/suno-mcp
- sandraschi/suno-mcp lineage
- AceDataCloud/SunoMCP
- CodeKeanu/suno-mcp
- alxTools/suno-mcp-server
- lioensky/MCP-Suno
- frankxai/suno-mcp-server

## Provider roles

A provider may have multiple roles:
- generator
- transformer
- workflow engine
- model fabric
- local engine
- design document
- scene editor
- game engine
- audio studio
- publisher
- analytics
- archive
- trainer

## Categories

- image
- video
- audio/music
- voice/speech
- 3D
- design
- animation/motion
- game/interactive
- local workflows
- model fabrics
- publishing/distribution
- analytics/growth
- archive/recovery

Provider category membership is many-to-many.
