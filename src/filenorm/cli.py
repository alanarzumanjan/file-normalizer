import argparse


def parse_arguments():
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
            "Text casing style: lower, upper, "
            "title (Each Word Capitalized), or capitalize"
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
        default="",
        help="Add a fixed prefix to file names",
    )

    parser.add_argument(
        "-x",
        "--suf",
        "--suffix",
        dest="suffix",
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
        help="Save rename history to filenorm_log.txt in target directory",
    )

    parser.add_argument(
        "--install",
        action="store_true",
        help="Install filenorm to user PATH (Windows)",
    )

    return parser