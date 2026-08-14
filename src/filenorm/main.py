#!/usr/bin/env python3

import os, argparse
from os.path import isfile
import string as s
import unicodedata
from filenorm.translit import transliterate

def parse_arguments():
    parser = argparse.ArgumentParser(description="Normalize file names by converting to lowercase," \
                        " replacing spaces, and removing unsupported characters.")
    parser.add_argument("path", type=str, nargs="?", default=".",
                        help="Target directory path (default: current directory)")
    parser.add_argument("-r", "--recursive", action="store_true",
                        help="Process directories recursively")
    parser.add_argument("-d", "--dry-run",
                        action="store_true",
                        help="Show changes without actually renaming files")
    parser.add_argument("--install", action="store_true", 
                        help="Install filenorm to user PATH (Windows)")
    return parser.parse_args()

def normalize_name(name, allowed_chars):
    transliterated = transliterate(name)
    normalized = unicodedata.normalize('NFKD', transliterated)
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

def main():
    args = parse_arguments()
    allowed_chars = set(s.ascii_lowercase + s.digits + '_')
    target_path = args.path
    
    if args.install:
        from filenorm.installer import install_for_windows
        install_for_windows()
        return

    if args.recursive:
        walker = os.walk(target_path, topdown=False)
    else:
        walker = [(target_path, [], os.listdir(target_path))]

    for current_dir, _, files in walker:
        for filename in files:
            file_path = os.path.join(current_dir, filename)
            
            if os.path.isdir(file_path):
                continue
            
            name, ext = os.path.splitext(filename)

            new_name = normalize_name(name, allowed_chars)
            new_ext = ext.replace(' ', '_').lower()
            new_filename = new_name + new_ext

            if filename != new_filename:
                new_file_path = os.path.join(current_dir, new_filename)
           
                if args.dry_run:
                    print(f"[DRY RUN] \"{filename}\" => \"{new_filename}\"")
                else:
                    os.rename(file_path, new_file_path)
                    print(f"\"{filename}\" => \"{new_filename}\"")

if __name__ == "__main__":
    main()