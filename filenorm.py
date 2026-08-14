import os, argparse
import string as s
import unicodedata

def parse_arguments():
    parser = argparse.ArgumentParser(description="Normalize file names by converting to lowercase, replacing spaces, and removing unsupported characters.")
    parser.add_argument("path", type=str, nargs="?", default=".",
                        help="Target directory path (default: current directory)")
    parser.add_argument("-r", "--recursive", action="store_true",
                        help="Process directories recursively")
    parser.add_argument("-d", "--dry-run",
                        action="store_true",
                        help="Show changes without actually renaming files")
    return parser.parse_args()

