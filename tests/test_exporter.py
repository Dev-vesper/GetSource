from src.internals.exporter import build_markdown, lang_for, write_markdown


def test_lang_for_known_extension():
    assert lang_for("a.py") == "python"
    assert lang_for("a.js") == "javascript"
    assert lang_for("a.cpp") == "cpp"
    assert lang_for("a.md") == "markdown"


def test_lang_for_known_name():
    assert lang_for("Dockerfile") == "dockerfile"
    assert lang_for("Makefile") == "makefile"
    assert lang_for(".gitignore") == "text"
    assert lang_for(".env") == "bash"


def test_lang_for_unknown():
    assert lang_for("a.xyz") == ""
    assert lang_for("a") == ""


def test_build_markdown_single_file(tmp_path):
    f = tmp_path / "a.py"
    f.write_text("print(1)\n")
    md = build_markdown([(str(f), "src/a.py")])
    assert md.startswith("### `src/a.py`\n\n````python\n")
    assert "print(1)" in md
    assert md.endswith("````")


def test_build_markdown_unknown_language(tmp_path):
    f = tmp_path / "a.xyz"
    f.write_text("data\n")
    md = build_markdown([(str(f), "a.xyz")])
    assert "````\n" in md


def test_build_markdown_adds_trailing_newline(tmp_path):
    f = tmp_path / "a.py"
    f.write_text("x = 1")
    md = build_markdown([(str(f), "a.py")])
    assert "x = 1\n````" in md


def test_build_markdown_multiple_files(tmp_path):
    f1 = tmp_path / "a.py"
    f2 = tmp_path / "b.txt"
    f1.write_text("A\n")
    f2.write_text("B\n")
    md = build_markdown([(str(f1), "a.py"), (str(f2), "b.txt")])
    assert "### `a.py`" in md
    assert "### `b.txt`" in md
    assert "````python\n" in md
    assert "````text\n" in md


def test_build_markdown_handles_unicode(tmp_path):
    f = tmp_path / "a.py"
    f.write_text("س = 1\n", encoding="utf-8")
    md = build_markdown([(str(f), "a.py")])
    assert "س = 1" in md


def test_build_markdown_handles_binary_as_text(tmp_path):
    f = tmp_path / "a.bin"
    f.write_bytes(b"\xff\xfe\x00\x01")
    md = build_markdown([(str(f), "a.bin")])
    assert "### `a.bin`" in md


def test_build_markdown_empty_file(tmp_path):
    f = tmp_path / "empty.py"
    f.write_text("")
    md = build_markdown([(str(f), "empty.py")])
    assert "````python\n````" in md


def test_write_markdown(tmp_path):
    f = tmp_path / "a.py"
    f.write_text("x = 1\n")
    out = tmp_path / "out.md"
    write_markdown([(str(f), "a.py")], str(out))
    saved = out.read_text(encoding="utf-8")
    assert saved.startswith("### `a.py`")
    assert "````python" in saved
