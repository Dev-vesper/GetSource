from pathlib import Path


def scan_folder(folder):
    folder = Path(folder)
    if not folder.is_dir():
        return []
    return sorted(p for p in folder.rglob("*") if p.is_file())


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
