#!/usr/bin/env python3

import argparse, sys
from filenorm.notification import print_error, print_example
from filenorm.processor import process_directory

def parse_arguments():
    parser = argparse.ArgumentParser(
        description=(
            "Normalize file names by configuring case styles, "
            "word separators, and removing unsupported characters."
        )
    )
    parser.add_argument("path", type=str, nargs="?", default=None,
                        help="Target directory path")
    parser.add_argument("-r", "--recursive", action="store_true",
                        help="Process directories recursively")
    parser.add_argument("-d", "--dry-run", action="store_true",
                        help="Show changes without actually renaming files")
    parser.add_argument("-c", "--case", choices=["lower", "upper", "title", "capitalize"], default="lower",
                        help="Text casing style: lower, upper, title (Each Word Capitalized), or capitalize")
    parser.add_argument("-s", "--separator", choices=["snake", "kebab", "space"], default="snake",
                        help="Word separator style: snake (underscores), kebab (hyphens), or space")
    parser.add_argument("-p", "--pref", "--prefix", dest="prefix", type=str, default="",
                        help="Add a fixed prefix to file names")
    parser.add_argument("-x", "--suf","--suffix", dest="suffix", type=str, default="",
                        help="Add a fixed suffix to file names (before extension)")
    parser.add_argument("-i", "--interactive", action="store_true",
                        help="Prompt for confirmation before renaming each file")
    parser.add_argument("-e", "--exclude", nargs="*", default=[],
                        help="Exclude files by extension or pattern (e.g., -e .mp3 .txt)")
    parser.add_argument("-l", "--log", action="store_true",
                        help="Save rename history to filenorm_log.txt in target directory")
    parser.add_argument("--install", action="store_true", 
                        help="Install filenorm to user PATH (Windows)")

    return parser, parser.parse_args()

def main():
    parser, args = parse_arguments()

    if args.install:
        from filenorm.installer import install_for_windows
        install_for_windows()
        return
    
    if len(sys.argv) == 1:
        parser.print_help()
        return

    if not args.path:
        print_error("You forgot to specify the directory path!")
        print_example("filenorm -s kebab .")
        return
    
    # Delegate execution to processor module
    process_directory(args)

if __name__ == "__main__":
    main()