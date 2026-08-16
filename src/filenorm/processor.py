import os
from datetime import datetime
from filenorm.core import split_filename, normalize_name
from filenorm.notification import print_error

def process_directory(args):
    target_path = args.path

    if args.recursive:
        walker = os.walk(target_path, topdown=False)
    else:
        walker = [(target_path, [], os.listdir(target_path))]

    changed = 0
    log_records = []

    for current_dir, _, files in walker:
        for filename in files:
            file_path = os.path.join(current_dir, filename)
            
            if not should_process(filename, file_path, args.exclude):
                continue
            
            name, extension = split_filename(filename)

            new_name = normalize_name(
                name,
                args.separator,
                args.case,
                args.prefix,
                args.suffix,
            )
            new_extension = extension.replace(' ', '_').lower()
            new_filename = new_name + new_extension

            if filename != new_filename:
                new_file_path = os.path.join(current_dir, new_filename)

                if args.interactive and not args.dry_run:
                    response = input(
                        f"Rename \"{filename}\" => \"{new_filename}\"? [Y/n]: "
                    ).strip().lower()

                    if response in ("n", "no"):
                        continue

                if args.dry_run:
                    record = f"[DRY RUN] \"{filename}\" => \"{new_filename}\""
                else:
                    if os.path.exists(new_file_path):
                        print_error(
                            f"Cannot rename \"{filename}\": "
                            f"\"{new_filename}\" already exists."
                        )
                        continue
                    os.rename(file_path, new_file_path)
                    record = f"\"{filename}\" => \"{new_filename}\""

                changed += 1
                print(record)
                log_records.append(record)

    if changed == 0:
        message = "Nothing to do. Everything is already formatted."
        print(message)
        log_records.append(message)

    if args.log:
        log_file_path = os.path.join(target_path, "filenorm_log.txt")
        try:
            with open(log_file_path, "a", encoding="utf-8") as f:
                f.write(f"\n--- Filenorm Report ({datetime.now().strftime('%Y-%m-%d %H:%M:%S')}) ---\n")
                f.write(f"Target: {os.path.abspath(target_path)}\n\n")
                for rec in log_records:
                    f.write(rec + "\n")
            print(f"\033[92m[LOG]\033[0m Report appended to {log_file_path}")

        except OSError as error:
            print_error(f"Failed to save log file: {error}")

def is_excluded(filename, exclusions):
    filename_lower = filename.lower()

    return any(
        pattern.lower() in filename_lower
        for pattern in exclusions
    )

def should_process(filename, file_path, exclusions):
    if os.path.isdir(file_path):
        return False

    if filename.startswith("."):
        return False

    # Never process filenorm's own log file.
    if filename.lower() == "filenorm_log.txt":
        return False

    return not is_excluded(filename, exclusions)