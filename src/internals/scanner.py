import os
from pathlib import Path

SKIP_DIRS = {
    "__pycache__",
    ".git",
    ".hg",
    ".svn",
    ".idea",
    ".vscode",
    ".mypy_cache",
    ".pytest_cache",
    ".ruff_cache",
    ".tox",
    ".nox",
    ".cache",
    "node_modules",
    ".venv",
    "venv",
    "env",
    ".env",
    "dist",
    "build",
    ".next",
    ".nuxt",
    "target",
}


def scan_folder(folder):
    folder = Path(folder)
    if not folder.is_dir():
        return []
    result = []
    for root, dirs, files in os.walk(folder, followlinks=False):
        dirs[:] = [d for d in dirs if d not in SKIP_DIRS]
        base = Path(root)
        for name in files:
            candidate = base / name
            if candidate.is_symlink():
                continue
            result.append(candidate)
    return sorted(result)


def parse_extensions(text):
    items = []
    for chunk in text.replace(";", ",").split(","):
        chunk = chunk.strip().lstrip(".").lower()
        if chunk:
            items.append(chunk)
    return items


def matches_extension(path, extensions):
    if not extensions:
        return False
    suffix = Path(path).suffix.lower().lstrip(".")
    return suffix in set(extensions)
