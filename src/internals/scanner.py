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
    for path in folder.rglob("*"):
        if any(part in SKIP_DIRS for part in path.parts):
            continue
        if path.is_file():
            result.append(path)
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
