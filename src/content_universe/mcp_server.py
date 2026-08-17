from __future__ import annotations

import argparse
from pathlib import Path

from .query import CatalogQuery


def run(db_path: str | Path) -> None:
    try:
        from mcp.server.fastmcp import FastMCP
    except ImportError as exc:
        raise SystemExit("Install MCP support with: pip install 'content-universe[mcp]'") from exc

    query = CatalogQuery(db_path)
    mcp = FastMCP("Content Universe")

    @mcp.tool()
    def catalog_stats() -> dict[str, int]:
        """Return entity counts in the Content Universe catalog."""
        return query.stats()

    @mcp.tool()
    def get_generation(request_id: str) -> dict | None:
        """Return one canonical generation by request ID."""
        return query.generation(request_id)

    @mcp.tool()
    def get_response(response_id: str) -> dict | None:
        """Return one canonical response by response ID."""
        return query.response(response_id)

    @mcp.tool()
    def get_asset(asset_id: str) -> dict | None:
        """Return one canonical asset by asset ID."""
        return query.asset(asset_id)

    @mcp.tool()
    def get_collection(collection_id: str) -> dict | None:
        """Return one reference collection by ID."""
        return query.collection(collection_id)

    @mcp.tool()
    def get_profile(key_or_handle: str) -> dict | None:
        """Return one profile by user ID or handle."""
        return query.profile(key_or_handle)

    @mcp.tool()
    def get_creative_entity(entity_key: str) -> dict | None:
        """Return a project/series/story/character/track/etc. by typed entity key."""
        return query.creative_entity(entity_key)

    @mcp.tool()
    def search_prompts(text: str, limit: int = 20) -> list[dict]:
        """Search normalized generation payloads for prompt/content text."""
        return query.search_prompts(text, limit)

    @mcp.tool()
    def search_entities(text: str, limit: int = 20) -> list[dict]:
        """Search project-level creative entities by title/metadata."""
        return query.search_entities(text, limit)

    @mcp.tool()
    def entity_kind_counts() -> dict[str, int]:
        """Return counts grouped by project-level creative entity kind."""
        return query.entity_kind_counts()

    @mcp.tool()
    def model_counts() -> dict[str, int]:
        """Return generation counts grouped by model version."""
        return query.model_counts()

    @mcp.tool()
    def request_type_counts() -> dict[str, int]:
        """Return counts grouped by generation request type."""
        return query.request_type_counts()

    @mcp.tool()
    def lineage(entity_key: str) -> list[dict]:
        """Return incoming/outgoing graph edges for any typed entity key."""
        return query.lineage(entity_key)

    @mcp.tool()
    def provenance(entity_key: str) -> list[dict]:
        """Return source observations for a canonical entity."""
        return query.provenance(entity_key)

    @mcp.tool()
    def assets_for_response(response_id: str) -> list[dict]:
        """Return known asset representations attached to a response."""
        return query.assets_for_response(response_id)

    mcp.run()


def main() -> None:
    parser = argparse.ArgumentParser(prog="content-universe-mcp")
    parser.add_argument("--db", default="content-universe.sqlite", help="SQLite catalog path")
    args = parser.parse_args()
    run(args.db)


if __name__ == "__main__":
    main()
