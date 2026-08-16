import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))

from filenorm.processor import process_directory


def create_args(
    path,
    recursive=False,
    dry_run=False,
    case="lower",
    separator="snake",
    prefix="",
    suffix="",
    interactive=False,
    exclude=None,
    log=False,
):
    return type(
        "Args",
        (),
        {
            "path": str(path),
            "recursive": recursive,
            "dry_run": dry_run,
            "case": case,
            "separator": separator,
            "prefix": prefix,
            "suffix": suffix,
            "interactive": interactive,
            "exclude": exclude or [],
            "log": log,
        },
    )()


def test_process_directory_renames_files(tmp_path):
    source = tmp_path / "My Cool File.TXT"
    source.write_text("test")

    args = create_args(tmp_path)

    process_directory(args)

    assert not source.exists()
    assert (tmp_path / "my_cool_file.txt").exists()


def test_dry_run_does_not_rename_files(tmp_path):
    source = tmp_path / "My Cool File.TXT"
    source.write_text("test")

    args = create_args(
        tmp_path,
        dry_run=True,
    )

    process_directory(args)

    assert source.exists()
    assert not (tmp_path / "my_cool_file.txt").exists()


def test_recursive_processing(tmp_path):
    nested_dir = tmp_path / "nested"
    nested_dir.mkdir()

    source = nested_dir / "My File.TXT"
    source.write_text("test")

    args = create_args(
        tmp_path,
        recursive=True,
    )

    process_directory(args)

    assert not source.exists()
    assert (nested_dir / "my_file.txt").exists()


def test_exclude_files(tmp_path):
    included = tmp_path / "My File.txt"
    excluded = tmp_path / "Music.mp3"

    included.write_text("test")
    excluded.write_text("music")

    args = create_args(
        tmp_path,
        exclude=[".mp3"],
    )

    process_directory(args)

    assert not included.exists()
    assert (tmp_path / "my_file.txt").exists()

    assert excluded.exists()


def test_existing_file_is_not_overwritten(tmp_path):
    source = tmp_path / "My File.txt"
    target = tmp_path / "my_file.txt"

    source.write_text("original")
    target.write_text("important")

    args = create_args(tmp_path)

    process_directory(args)

    assert source.exists()
    assert target.exists()

    assert source.read_text() == "original"
    assert target.read_text() == "important"


def test_interactive_mode_accepts_rename(tmp_path, monkeypatch):
    source = tmp_path / "My File.txt"
    source.write_text("test")

    monkeypatch.setattr("builtins.input", lambda _: "")

    args = create_args(
        tmp_path,
        interactive=True,
    )

    process_directory(args)

    assert not source.exists()
    assert (tmp_path / "my_file.txt").exists()


def test_interactive_mode_can_skip_rename(tmp_path, monkeypatch):
    source = tmp_path / "My File.txt"
    source.write_text("test")

    monkeypatch.setattr("builtins.input", lambda _: "n")

    args = create_args(
        tmp_path,
        interactive=True,
    )

    process_directory(args)

    assert source.exists()
    assert not (tmp_path / "my_file.txt").exists()


def test_log_file_is_created(tmp_path):
    source = tmp_path / "My File.txt"
    source.write_text("test")

    args = create_args(
        tmp_path,
        log=True,
    )

    process_directory(args)

    log_file = tmp_path / "filenorm_log.txt"

    assert log_file.exists()

    content = log_file.read_text(encoding="utf-8")

    assert "My File.txt" in content
    assert "my_file.txt" in content


def test_log_file_is_not_processed(tmp_path):
    log_file = tmp_path / "filenorm_log.txt"
    log_file.write_text("previous log")

    args = create_args(tmp_path)

    process_directory(args)

    assert log_file.exists()
    assert log_file.read_text() == "previous log"


def test_prefix_and_suffix(tmp_path):
    source = tmp_path / "My File.txt"
    source.write_text("test")

    args = create_args(
        tmp_path,
        prefix="2026-",
        suffix="-final",
    )

    process_directory(args)

    assert not source.exists()
    assert (tmp_path / "2026-my_file-final.txt").exists()


def test_compound_extension_is_preserved(tmp_path):
    source = tmp_path / "My Archive.tar.gz"
    source.write_text("test")

    args = create_args(tmp_path)

    process_directory(args)

    assert not source.exists()
    assert (tmp_path / "my_archive.tar.gz").exists()