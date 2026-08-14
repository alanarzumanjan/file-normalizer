#!/usr/bin/env python3

import os, argparse
from filenorm.core import split_filename, normalize_name

def parse_arguments():
    parser = argparse.ArgumentParser(
        description=(
            "Normalize file names by configuring case styles, "
            "word separators, and removing unsupported characters."
        )
    )
    parser.add_argument("path", type=str, nargs="?", default=".",
                        help="Target directory path (default: current directory)")
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
    parser.add_argument("-i", "--install", action="store_true", 
                        help="Install filenorm to user PATH (Windows)")
    return parser.parse_args()

def main():
    args = parse_arguments()

    # Handle installation if it is windows
    if args.install:
        from filenorm.installer import install_for_windows
        install_for_windows()
        return
    
    target_path = args.path

    if args.recursive:
        walker = os.walk(target_path, topdown=False)
    else:
        walker = [(target_path, [], os.listdir(target_path))]

    # Process files in the specified directory (and subdirectories if recursive)
    for current_dir, _, files in walker:
        for filename in files:
            file_path = os.path.join(current_dir, filename)
            
            if os.path.isdir(file_path): # Skip directories
                continue
            
            name, ext = split_filename(filename)

            # Normalize the name and extension
            new_name = normalize_name(name, args.separator, args.case, args.prefix, args.suffix)
            new_ext = ext.replace(' ', '_').lower()
            new_filename = new_name + new_ext

            if filename != new_filename: # Rename if the new filename is different
                new_file_path = os.path.join(current_dir, new_filename)
           
                if args.dry_run:
                    print(f"[DRY RUN] \"{filename}\" => \"{new_filename}\"")
                else:
                    os.rename(file_path, new_file_path)
                    print(f"\"{filename}\" => \"{new_filename}\"")

if __name__ == "__main__":
    main()