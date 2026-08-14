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

def normalize_name(name, allowed_chars):
    normalized = unicodedata.normalize('NFKD', name)
    clean_chars = []

    for char in normalized:
        if char == ' ':
            clean_chars.append('_')
        else:
            lower_char = char.lower()
            if lower_char in allowed_chars:
                clean_chars.append(lower_char)
    
    new_name = ''.join(clean_chars)

    while '__' in new_name:
        new_name = new_name.replace('__', '_')
    
    return new_name.strip('_')
