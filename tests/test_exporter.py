from src.internals.exporter import build_markdown, write_markdown


def test_build_markdown_single_file(tmp_path):
    f = tmp_path / "a.py"
    f.write_text("print(1)")
    md = build_markdown([(str(f), "src/a.py")])
    assert md.startswith("```src/a.py")
    assert "print(1)" in md
    assert md.endswith("```")


def test_build_markdown_multiple_files(tmp_path):
    f1 = tmp_path / "a.py"
    f2 = tmp_path / "b.txt"
    f1.write_text("A")
    f2.write_text("B")
    md = build_markdown([(str(f1), "a.py"), (str(f2), "b.txt")])
    assert "```a.py" in md
    assert "```b.txt" in md
    assert md.count("```") == 4


def test_write_markdown(tmp_path):
    f = tmp_path / "a.py"
    f.write_text("x = 1")
    out = tmp_path / "out.md"
    write_markdown([(str(f), "a.py")], str(out))
    assert out.read_text(encoding="utf-8").startswith("```a.py")
