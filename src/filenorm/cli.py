import argparse
import sys


def _normalize_negative_values(arguments):
    """
    Allow option values that start with '-'.

    For example:
        --suffix "-final"
        -x "-v1"

    are converted internally to:
        --suffix=-final
        -x=-v1
    """

    value_options = {
        "-p",
        "--pref",
        "--prefix",
        "-x",
        "--suf",
        "--suffix",
    }

    normalized = []
    i = 0

    while i < len(arguments):
        argument = arguments[i]

        if argument in value_options and i + 1 < len(arguments):
            value = arguments[i + 1]

            if value.startswith("-") and value not in value_options:
                normalized.append(f"{argument}={value}")
                i += 2
                continue

        normalized.append(argument)
        i += 1

    return normalized


def create_parser():
    parser = argparse.ArgumentParser(
        description=(
            "Normalize file names by configuring case styles, "
            "word separators, and removing unsupported characters."
        )
    )

    parser.add_argument(
        "path",
        nargs="?",
        help="Target directory path",
    )

    parser.add_argument(
        "-r",
        "--recursive",
        action="store_true",
        help="Process directories recursively",
    )

    parser.add_argument(
        "-d",
        "--dry-run",
        action="store_true",
        help="Show changes without actually renaming files",
    )

    parser.add_argument(
        "-c",
        "--case",
        choices=["lower", "upper", "title", "capitalize"],
        default="lower",
        help=(
            "Text casing style: lower, upper, title "
            "(Each Word Capitalized), or capitalize"
        ),
    )

    parser.add_argument(
        "-s",
        "--separator",
        choices=["snake", "kebab", "space"],
        default="snake",
        help=(
            "Word separator style: snake (underscores), "
            "kebab (hyphens), or space"
        ),
    )

    parser.add_argument(
        "-p",
        "--pref",
        "--prefix",
        dest="prefix",
        type=str,
        default="",
        help="Add a fixed prefix to file names",
    )

    parser.add_argument(
        "-x",
        "--suf",
        "--suffix",
        dest="suffix",
        type=str,
        default="",
        help="Add a fixed suffix to file names (before extension)",
    )

    parser.add_argument(
        "-i",
        "--interactive",
        action="store_true",
        help="Prompt for confirmation before renaming each file",
    )

    parser.add_argument(
        "-e",
        "--exclude",
        nargs="*",
        default=[],
        help=(
            "Exclude files by extension or pattern "
            "(e.g., -e .mp3 .txt)"
        ),
    )

    parser.add_argument(
        "-l",
        "--log",
        action="store_true",
        help=(
            "Save rename history to filenorm_log.txt "
            "in target directory"
        ),
    )

    parser.add_argument(
        "--install",
        action="store_true",
        help="Install filenorm to user PATH (Windows)",
    )

    return parser


def parse_arguments(arguments=None):
    """
    Parse command-line arguments.

    Supports values beginning with '-' for prefix and suffix options.
    """

    if arguments is None:
        arguments = sys.argv[1:]

    arguments = _normalize_negative_values(arguments)

    parser = create_parser()

    return parser.parse_args(arguments)