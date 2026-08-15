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

    changes_count = 0
    log_records = []

    for current_dir, _, files in walker:
        for filename in files:
            file_path = os.path.join(current_dir, filename)
            
            if os.path.isdir(file_path):
                continue

            if filename.startswith('.'):
                continue

            if filename.lower() in ('filenorm_log.txt', 'filenorm_history.txt'):
                continue

            if args.exclude:
                is_excluded = False
                for exc in args.exclude:
                    exc_lower = exc.lower()
                    filename_lower = filename.lower()
                    if filename_lower.endswith(exc_lower) or exc_lower in filename_lower:
                        is_excluded = True
                        break
                if is_excluded:
                    continue
            
            name, ext = split_filename(filename)

            new_name = normalize_name(name, args.separator, args.case, args.prefix, args.suffix)
            new_ext = ext.replace(' ', '_').lower()
            new_filename = new_name + new_ext

            if filename != new_filename:
                new_file_path = os.path.join(current_dir, new_filename)

                # Interactive prompt check
                if args.interactive and not args.dry_run:
                    response = input(f"Rename \"{filename}\" => \"{new_filename}\"? [Y/n]: ").strip().lower()
                    if response in ('n', 'no'):
                        continue  # Skip if user answered anything other than no

                changes_count += 1

                if args.dry_run:
                    record = f"[DRY RUN] \"{filename}\" => \"{new_filename}\""
                else:
                    os.rename(file_path, new_file_path)
                    record = f"\"{filename}\" => \"{new_filename}\""

                print(record)
                log_records.append(record)

    if changes_count == 0:
        message = "Nothing to do. Everything is already formatted."
        print(message)
        log_records.append(message)

    # Save log file if requested
    if args.log:
        log_file_path = os.path.join(target_path, "filenorm_log.txt")
        try:
            with open(log_file_path, "a", encoding="utf-8") as f:
                f.write(f"\n--- Filenorm Report ({datetime.now().strftime('%Y-%m-%d %H:%M:%S')}) ---\n")
                f.write(f"Target: {os.path.abspath(target_path)}\n\n")
                for rec in log_records:
                    f.write(rec + "\n")
            print(f"\033[92m[LOG]\033[0m Report appended to {log_file_path}")
        except Exception as e:
            print_error(f"Failed to save log file: {e}")