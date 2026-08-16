#!/usr/bin/env python3

import sys

from filenorm.cli import create_parser, parse_arguments
from filenorm.notification import print_error, print_example
from filenorm.processor import process_directory


def main():
    if len(sys.argv) == 1:
        create_parser().print_help()
        return

    args = parse_arguments()

    if args.install:
        from filenorm.installer import install_for_windows

        install_for_windows()
        return

    if not args.path:
        print_error("You forgot to specify the directory path!")
        print_example("filenorm -s kebab .")
        return

    process_directory(args)


if __name__ == "__main__":
    main()