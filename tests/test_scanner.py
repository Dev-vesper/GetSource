from src.internals.scanner import matches_extension, parse_extensions, scan_folder


def test_parse_extensions_basic():
    assert parse_extensions("py, ml") == ["py", "ml"]


def test_parse_extensions_dots_and_semicolons():
    assert parse_extensions(".py;.js") == ["py", "js"]


def test_parse_extensions_empty():
    assert parse_extensions("") == []
    assert parse_extensions(" , , ") == []


def test_matches_extension():
    assert matches_extension("a/b/file.py", ["py", "ml"])
    assert not matches_extension("a/b/file.txt", ["py", "ml"])
    assert not matches_extension("a/b/file", [])


def test_scan_folder_recursive(tmp_path):
    (tmp_path / "a.py").write_text("a")
    (tmp_path / "b.txt").write_text("b")
    sub = tmp_path / "sub"
    sub.mkdir()
    (sub / "c.py").write_text("c")

    files = scan_folder(tmp_path)
    names = sorted(p.name for p in files)
    assert names == ["a.py", "b.txt", "c.py"]


def test_scan_folder_skips_common_dirs(tmp_path):
    (tmp_path / "a.py").write_text("a")
    for name in ("__pycache__", ".git", ".venv", "node_modules", "build"):
        d = tmp_path / name
        d.mkdir()
        (d / "junk.py").write_text("junk")

    files = scan_folder(tmp_path)
    names = [p.name for p in files]
    assert names == ["a.py"]


def test_scan_folder_returns_empty_for_file(tmp_path):
    f = tmp_path / "a.py"
    f.write_text("a")
    assert scan_folder(f) == []
