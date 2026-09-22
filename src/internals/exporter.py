from pathlib import Path

EXT_LANG = {
    "py": "python",
    "pyi": "python",
    "pyw": "python",
    "js": "javascript",
    "mjs": "javascript",
    "cjs": "javascript",
    "jsx": "jsx",
    "ts": "typescript",
    "tsx": "tsx",
    "java": "java",
    "kt": "kotlin",
    "kts": "kotlin",
    "c": "c",
    "h": "c",
    "cpp": "cpp",
    "cc": "cpp",
    "cxx": "cpp",
    "hpp": "cpp",
    "hh": "cpp",
    "hxx": "cpp",
    "cs": "csharp",
    "go": "go",
    "rs": "rust",
    "rb": "ruby",
    "php": "php",
    "swift": "swift",
    "m": "objectivec",
    "mm": "objectivec",
    "scala": "scala",
    "sh": "bash",
    "bash": "bash",
    "zsh": "bash",
    "fish": "fish",
    "ps1": "powershell",
    "bat": "batch",
    "cmd": "batch",
    "html": "html",
    "htm": "html",
    "xml": "xml",
    "svg": "xml",
    "css": "css",
    "scss": "scss",
    "sass": "sass",
    "less": "less",
    "json": "json",
    "jsonc": "json",
    "yaml": "yaml",
    "yml": "yaml",
    "toml": "toml",
    "ini": "ini",
    "cfg": "ini",
    "conf": "ini",
    "md": "markdown",
    "markdown": "markdown",
    "rst": "rst",
    "tex": "latex",
    "sql": "sql",
    "graphql": "graphql",
    "gql": "graphql",
    "proto": "protobuf",
    "txt": "text",
    "log": "text",
    "csv": "csv",
    "tsv": "text",
    "lua": "lua",
    "r": "r",
    "jl": "julia",
    "dart": "dart",
    "ex": "elixir",
    "exs": "elixir",
    "erl": "erlang",
    "hrl": "erlang",
    "hs": "haskell",
    "clj": "clojure",
    "cljs": "clojure",
    "cljc": "clojure",
    "vue": "vue",
    "svelte": "svelte",
    "astro": "astro",
    "tf": "hcl",
    "hcl": "hcl",
    "nix": "nix",
    "cmake": "cmake",
    "mk": "makefile",
    "asm": "asm",
    "s": "asm",
    "zig": "zig",
    "nim": "nim",
    "v": "v",
    "pas": "pascal",
    "pl": "perl",
    "pm": "perl",
}

NAME_LANG = {
    "dockerfile": "dockerfile",
    "makefile": "makefile",
    "cmakelists.txt": "cmake",
    "rakefile": "ruby",
    "gemfile": "ruby",
    "vagrantfile": "ruby",
    ".gitignore": "text",
    ".gitattributes": "text",
    ".dockerignore": "text",
    ".editorconfig": "ini",
    ".env": "bash",
    ".bashrc": "bash",
    ".zshrc": "bash",
    ".profile": "bash",
    "license": "text",
    "readme": "markdown",
}


def lang_for(path):
    p = Path(path)
    key = p.name.lower()
    if key in NAME_LANG:
        return NAME_LANG[key]
    ext = p.suffix.lower().lstrip(".")
    return EXT_LANG.get(ext, "")


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
        if content and not content.endswith("\n"):
            content += "\n"
        lang = lang_for(path)
        parts.append(f"### `{display}`\n\n````{lang}\n{content}````")
    return "\n\n".join(parts)


def write_markdown(entries, output_path):
    data = build_markdown(entries)
    Path(output_path).write_text(data, encoding="utf-8")
    return data
