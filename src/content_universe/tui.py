from __future__ import annotations

import argparse
import json

from .query import CatalogQuery


def main() -> None:
    try:
        from textual.app import App, ComposeResult
        from textual.containers import Horizontal
        from textual.widgets import Footer, Header, Input, Static, Tree
    except ImportError as exc:
        raise SystemExit("Install TUI support with: pip install 'content-universe[tui]'") from exc

    parser = argparse.ArgumentParser(prog="content-universe-tui")
    parser.add_argument("--db", default="content-universe.sqlite")
    args = parser.parse_args()
    query = CatalogQuery(args.db)

    class UniverseApp(App):
        CSS = """
        #results { width: 42%; border: round $accent; }
        #detail { width: 58%; border: round $primary; padding: 1 2; overflow: auto; }
        #search { dock: top; }
        """
        BINDINGS = [("q", "quit", "Quit"), ("ctrl+l", "clear", "Clear")]

        def compose(self) -> ComposeResult:
            yield Header()
            yield Input(placeholder="Search prompts, captions, metadata…", id="search")
            with Horizontal():
                yield Tree("Content Universe", id="results")
                yield Static("Search the catalog to begin.", id="detail")
            yield Footer()

        def on_mount(self) -> None:
            tree = self.query_one("#results", Tree)
            models = tree.root.add("Models")
            for model, count in query.model_counts().items():
                models.add_leaf(f"{model} ({count})")
            tree.root.expand()

        async def on_input_submitted(self, event: Input.Submitted) -> None:
            tree = self.query_one("#results", Tree)
            tree.clear()
            root = tree.root
            root.set_label(f"Results: {event.value}")
            for item in query.search_prompts(event.value, 50):
                root.add_leaf(item.get("request_id", "<unknown>"), data=item)
            root.expand()

        def on_tree_node_selected(self, event: Tree.NodeSelected) -> None:
            if event.node.data:
                self.query_one("#detail", Static).update(json.dumps(event.node.data, indent=2, ensure_ascii=False))

        def action_clear(self) -> None:
            self.query_one("#search", Input).value = ""
            self.query_one("#detail", Static).update("Search cleared.")

    UniverseApp().run()


if __name__ == "__main__":
    main()
