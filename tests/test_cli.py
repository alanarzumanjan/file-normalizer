import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))

from filenorm.cli import parse_arguments


def parse_args(arguments):
    return parse_arguments(arguments)


def test_default_arguments():
    args = parse_args(["."])

    assert args.path == "."
    assert args.recursive is False
    assert args.dry_run is False
    assert args.case == "lower"
    assert args.separator == "snake"
    assert args.prefix == ""
    assert args.suffix == ""
    assert args.interactive is False
    assert args.exclude == []
    assert args.log is False
    assert args.install is False


def test_case_and_separator_arguments():
    args = parse_args(
        [
            ".",
            "--case",
            "title",
            "--separator",
            "kebab",
        ]
    )

    assert args.case == "title"
    assert args.separator == "kebab"


def test_short_case_and_separator_arguments():
    args = parse_args(
        [
            ".",
            "-c",
            "upper",
            "-s",
            "space",
        ]
    )

    assert args.case == "upper"
    assert args.separator == "space"


def test_prefix_and_suffix_arguments():
    args = parse_args(
        [
            ".",
            "--prefix",
            "2026-",
            "--suffix",
            "-final",
        ]
    )

    assert args.prefix == "2026-"
    assert args.suffix == "-final"


def test_short_prefix_and_suffix_arguments():
    args = parse_args(
        [
            ".",
            "-p",
            "project-",
            "-x",
            "-v1",
        ]
    )

    assert args.prefix == "project-"
    assert args.suffix == "-v1"


def test_prefix_and_suffix_with_equals():
    args = parse_args(
        [
            ".",
            "--prefix=2026-",
            "--suffix=-final",
        ]
    )

    assert args.prefix == "2026-"
    assert args.suffix == "-final"


def test_short_prefix_and_suffix_with_equals():
    args = parse_args(
        [
            ".",
            "-p=project-",
            "-x=-v1",
        ]
    )

    assert args.prefix == "project-"
    assert args.suffix == "-v1"


def test_boolean_arguments():
    args = parse_args(
        [
            ".",
            "--recursive",
            "--dry-run",
            "--interactive",
            "--log",
        ]
    )

    assert args.recursive is True
    assert args.dry_run is True
    assert args.interactive is True
    assert args.log is True


def test_exclude_argument():
    args = parse_args(
        [
            ".",
            "--exclude",
            ".mp3",
            ".txt",
        ]
    )

    assert args.exclude == [".mp3", ".txt"]


def test_install_argument():
    args = parse_args(
        [
            "--install",
        ]
    )

    assert args.install is True


@pytest.mark.parametrize(
    "case_style",
    [
        "lower",
        "upper",
        "title",
        "capitalize",
    ],
)

def test_valid_case_styles(case_style):
    args = parse_args(
        [
            ".",
            "--case",
            case_style,
        ]
    )

    assert args.case == case_style


@pytest.mark.parametrize(
    "separator_style",
    [
        "snake",
        "kebab",
        "space",
    ],
)

def test_valid_separator_styles(separator_style):
    args = parse_args(
        [
            ".",
            "--separator",
            separator_style,
        ]
    )

    assert args.separator == separator_style