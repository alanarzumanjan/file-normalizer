#!/usr/bin/env python3

import os, argparse
from filenorm.core import split_filename, get_allowed_chars, normalize_name

# Arguments definition and parsing
def parse_arguments():
    parser = argparse.ArgumentParser(description="Normalize file names by converting case," \
                        " replacing spaces, and removing unsupported characters.")
    parser.add_argument("path", type=str, nargs="?", default=".",
                        help="Target directory path (default: current directory)")
    parser.add_argument("-r", "--recursive", action="store_true",
                        help="Process directories recursively")
    parser.add_argument("-d", "--dry-run", action="store_true",
                        help="Show changes without actually renaming files")
    parser.add_argument("--case", choices=["snake", "kebab", "lower"], default="snake",
                        help="Naming case style: snake (underscores), kebab (hyphens)," \
                        " or lower (lowercase with spaces)")
    parser.add_argument("--prefix", type=str, default="",
                        help="Add a fixed prefix to file names")
    parser.add_argument("--suffix", type=str, default="",
                        help="Add a fixed suffix to file names (before extension)")
    parser.add_argument("--install", action="store_true", 
                        help="Install filenorm to user PATH (Windows)")
    return parser.parse_args()

# Main function
def main():
    args = parse_arguments()

    # Handle installation if it is windows
    if args.install:
        from filenorm.installer import install_for_windows
        install_for_windows()
        return
    
    # Get allowed characters based on the case style
    allowed_chars = get_allowed_chars(args.case)
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

            # Converting all
            new_name = normalize_name(name, allowed_chars, args.case, args.prefix, args.suffix)
            new_ext = ext.replace(' ', '_').lower()
            new_filename = new_name + new_ext

            if filename != new_filename: # Only rename if the new filename is different
                new_file_path = os.path.join(current_dir, new_filename)
           
                if args.dry_run:
                    print(f"[DRY RUN] \"{filename}\" => \"{new_filename}\"")
                else:
                    os.rename(file_path, new_file_path)
                    print(f"\"{filename}\" => \"{new_filename}\"")

if __name__ == "__main__":
    main()