from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Iterable

from .adapters import default_registry
from .adapters.base import AdapterRegistry


DEFAULT_IGNORED_DIRS = {
    ".git",
    ".hg",
    ".svn",
    ".idea",
    ".vscode",
    "__pycache__",
    "node_modules",
    ".venv",
    "venv",
    "dist",
    "build",
}


@dataclass(slots=True)
class FolderDiscovery:
    root: Path
    supported: list[Path] = field(default_factory=list)
    unsupported: list[Path] = field(default_factory=list)
    skipped: list[Path] = field(default_factory=list)

    def to_dict(self) -> dict[str, object]:
        return {
            "root": str(self.root),
            "supported_count": len(self.supported),
            "unsupported_count": len(self.unsupported),
            "skipped_count": len(self.skipped),
            "supported": [str(path) for path in self.supported],
            "unsupported": [str(path) for path in self.unsupported],
            "skipped": [str(path) for path in self.skipped],
        }


def _matches_any(path: Path, patterns: Iterable[str]) -> bool:
    return any(path.match(pattern) for pattern in patterns)


def discover_folder_sources(
    folder: str | Path,
    *,
    registry: AdapterRegistry | None = None,
    recursive: bool = True,
    include: Iterable[str] = (),
    exclude: Iterable[str] = (),
    ignored_dirs: Iterable[str] = DEFAULT_IGNORED_DIRS,
    max_files: int | None = None,
) -> FolderDiscovery:
    """Discover files in *folder* that can be handled by a registered adapter.

    Discovery is intentionally adapter-driven rather than extension-driven so new
    adapters automatically become eligible without changing this module.
    """
    root = Path(folder).expanduser().resolve()
    if not root.exists():
        raise FileNotFoundError(f"Folder does not exist: {root}")
    if not root.is_dir():
        raise NotADirectoryError(f"Not a directory: {root}")
    if max_files is not None and max_files < 1:
        raise ValueError("max_files must be >= 1")

    registry = registry or default_registry()
    include_patterns = tuple(include)
    exclude_patterns = tuple(exclude)
    ignored = set(ignored_dirs)
    result = FolderDiscovery(root=root)

    iterator = root.rglob("*") if recursive else root.glob("*")
    examined = 0

    for path in sorted(iterator):
        if not path.is_file():
            continue

        relative = path.relative_to(root)
        if any(part in ignored for part in relative.parts[:-1]):
            result.skipped.append(path)
            continue
        if include_patterns and not _matches_any(relative, include_patterns):
            result.skipped.append(path)
            continue
        if exclude_patterns and _matches_any(relative, exclude_patterns):
            result.skipped.append(path)
            continue

        examined += 1
        if max_files is not None and examined > max_files:
            break

        try:
            registry.resolve(path)
        except ValueError:
            result.unsupported.append(path)
        else:
            result.supported.append(path)

    return result
