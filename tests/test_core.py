import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))

from filenorm.core import normalize_name, split_filename


@pytest.mark.parametrize(
    "filename, case_style, separator_style, prefix, suffix, expected",
    [
        ("My Cool File.TXT", "lower", "snake", "", "", "my_cool_file.txt"),
        ("hello world.png", "upper", "snake", "", "", "HELLO_WORLD.png"),
        ("hello world.png", "title", "kebab", "", "", "Hello-World.png"),
        ("hello world.png", "capitalize", "space", "", "", "Hello world.png"),
        ("Archive File.tar.gz", "lower", "snake", "", "", "archive_file.tar.gz"),
        ("Script User.JS", "lower", "kebab", "", "", "script-user.js"),
        (
            "document.pdf",
            "lower",
            "snake",
            "2026-",
            "-v1",
            "2026-document-v1.pdf",
        ),
        (
            "Привет Миr.txt",
            "lower",
            "snake",
            "",
            "",
            "privet_mir.txt",
        ),
    ],
)
def test_normalize_filename(
    filename,
    case_style,
    separator_style,
    prefix,
    suffix,
    expected,
):
    name, extension = split_filename(filename)

    new_name = normalize_name(
        name,
        separator_style=separator_style,
        case_style=case_style,
        prefix=prefix,
        suffix=suffix,
    )

    new_extension = extension.replace(" ", "_").lower()
    result = new_name + new_extension

    assert result == expected


@pytest.mark.parametrize(
    "filename, expected_name, expected_extension",
    [
        ("document.pdf", "document", ".pdf"),
        ("image.PNG", "image", ".PNG"),
        ("archive.zip", "archive", ".zip"),
        ("README", "README", ""),
    ],
)
def test_split_filename(filename, expected_name, expected_extension):
    name, extension = split_filename(filename)

    assert name == expected_name
    assert extension == expected_extension


@pytest.mark.parametrize(
    "filename, expected_name, expected_extension",
    [
        ("backup.tar.gz", "backup", ".tar.gz"),
        ("archive.tar.bz2", "archive", ".tar.bz2"),
        ("archive.tar.xz", "archive", ".tar.xz"),
        ("script.user.js", "script", ".user.js"),
        ("metadata.meta.js", "metadata", ".meta.js"),
        ("types.d.ts", "types", ".d.ts"),
        ("bundle.min.js", "bundle", ".min.js"),
        ("config.config.json", "config", ".config.json"),
        ("config.config.yaml", "config", ".config.yaml"),
        ("server.log.gz", "server", ".log.gz"),
        ("backup.bak.gz", "backup", ".bak.gz"),
    ],
)
def test_split_compound_extensions(
    filename,
    expected_name,
    expected_extension,
):
    name, extension = split_filename(filename)

    assert name == expected_name
    assert extension == expected_extension