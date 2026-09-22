from pathlib import Path


def _read_text(path):
    try:
        return path.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        return path.read_text(encoding="utf-8", errors="replace")
    except OSError as exc:
        return f"[unable to read: {exc}]"


def build_markdown(entries):
    parts = []
    for path, display in entries:
        content = _read_text(Path(path))
        parts.append(f"```{display}\n{content}\n```")
    return "\n\n".join(parts)


def write_markdown(entries, output_path):
    data = build_markdown(entries)
    Path(output_path).write_text(data, encoding="utf-8")
    return data
