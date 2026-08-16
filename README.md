# File Normalizer (`filenorm`)

A lightweight, cross-platform command-line utility for cleaning up and normalizing file names.

`filenorm` standardizes file names by applying configurable case styles and word separators, adding custom prefixes and suffixes, transliterating characters, and protecting complex extensions.

<!-- <video controls width="100%">
  <source src="docs/preview2.mp4" type="video/mp4">
  Your browser can't preview this video
</video> -->

<!-- ![Preview](docs/preview2.gif) -->
<img src="docs/preview2.gif" width="100%" alt="Preview">

## Features

- **Flexible Case Styles (`-c`,`--case`)** — choose between `lower`, `upper`, `title` (Each Word Capitalized), or `capitalize`.
- **Word Separators (`-s`,`--separator`)** — choose how to separate words: `snake` (underscores), `kebab` (hyphens), or `space`.
- **Prefixes & Suffixes (`-p`,`-x`,`--pref`,`--suf`,`--prefix`, `--suffix`)** — add a fixed text at the beginning or end of each file (suffixes are smartly placed before the extension).
- **Smart Extension Protection** — keeps complex and compound extensions such as `.tar.gz`, `.user.js`, `.d.ts`, `.config.json`, `.min.js`, and `.log.gz` safe while normalizing only the file name.
- **Transliteration** — automatically converts non-Latin characters (like Cyrillic, Chinese, etc.) into standard Latin script using `unidecode`.
- **Special Character Removal** — removes unsupported or disruptive characters.
- **Recursive Mode (`-r`)** — processes files inside nested directories.
- **Dry-run Mode (`-d`)** — previews changes without renaming anything.
- **Exclude Files (`-e`, `--exclude`)** — skips files, extensions, or filename patterns from being processed.
- **History Logging (`-l`, `--log`)** — saves a timestamped rename report to `filenorm_log.txt` and prevents the log file from being renamed.
- **Interactive Mode (`-i`, `--interactive`)** — prompts for confirmation (`[Y/n]`) before renaming each file. Pressing Enter defaults to Yes.
- **Windows Installation (`--install`)** — installs the compiled executable to `%LOCALAPPDATA%\Filenorm` and adds it to the user's PATH.

## Installation

### Option 1: Install with `pip/x` — Recommended

**[Download Python](https://www.python.org/downloads/)** + and make sure Python and `pip` are available in your PATH.

If you have Python and `pip/x` installed, you can install `filenorm` globally in an isolated environment:

**Check downloads**

```bash
python --version
pip --version
```

**Install from repo**

```bash
pip install git+https://github.com/alanarzumanjan/file-normalizer.git
```

**You can install `filenorm` directly from PyPI:**

```bash
pip install filenorm
```

### Option 2: Standalone binaries

No Python installation is required when using the pre-compiled binaries.

Download the latest release from the [GitHub Releases](https://github.com/alanarzumanjan/file-normalizer/releases) page.

Available binaries:

- **Linux:** `filenorm-linux-amd64`
- **macOS:** `filenorm-macos-universal`

For macOS & Linux:
Download the binary and the install.sh script into the same folder, open your terminal there, and run:

```bash
bash install.sh
```

- **Windows:** `filenorm-windows-amd64.exe`

For Windows:

Open PowerShell in your Downloads directory and run:

```powershell
cd $HOME\Downloads
.\filenorm-windows-amd64.exe --install
```

### Option 3: Install for development

Clone the repository and install the package in editable mode:

```bash
git clone https://github.com/alanarzumanjan/file-normalizer.git
cd file-normalizer
pip install -e .
```

## Usage

```text
filenorm [path] [options]
```

### Arguments

| Argument | Description |
|---|---|
| `path` | Target directory. Defaults to the current working directory. |

### Options

| Option | Description |
|---|---|
| `-h`, `--help` | Show the help message and exit. |
| `-r`, `--recursive` | Process files in nested directories recursively. |
| `-d`, `--dry-run` | Preview changes without renaming files. |
| `-c`, `--case {lower,upper,title,capitalize}` | Text casing style (default: lower). |
| `-s`, `--separator {snake,kebab,space}` | Word separator style (default: snake). |
| `-p`, `--pref`, `--prefix TEXT` | Add a fixed prefix to file names. |
| `-x`, `--suf`, `--suffix TEXT` | Add a fixed suffix to file names (before extension). |
| `-e`, `--exclude [EXCLUDE ...]` | Exclude files by name, extension, or pattern (e.g., `-e .mp3 .txt`). |
| `-l`, `--log` | Save/append rename history to `filenorm_log.txt` in the target directory. |
| `-i`, `--interactive` | Prompt for confirmation (`[Y/n]`) before renaming each file. |
| `--install` | Installs the compiled executable to `%LOCALAPPDATA%\Filenorm` and adds it to the user's PATH (Windows). |

## Examples

### Preview Changes

Preview the changes that would be made in the current directory without modifying any files:

```bash
filenorm --dry-run
```

### Normalize Recursively

Process files in the target directory and all nested directories:

```bash
filenorm /path/to/your/music --recursive
```

### Use Custom Case and Separators

Convert names to Title Case with hyphens (kebab):

```bash
filenorm --case title --separator kebab
```

### Add Prefixes and Suffixes

Add a date prefix and a version suffix to all files:

```bash
filenorm --prefix "2026-08-" --suffix "-final"
```

**Note:** If a prefix or suffix value starts with `-`, use `=` to make it clear that the value belongs to the option.

```bash
filenorm --suffix=-final
filenorm -x=-v1
```

### All Combination

```bash
filenorm /path/to/your/files --recursive --case title --separator kebab --prefix "project-" --suffix "-v1" --dry-run
```

or Shortened Command Version:

```bash
filenorm /path/to/your/files -r -d -c title -s kebab -p "project-" -x "-v1"
```

### Current Directory Target

```bash
filenorm .
```

### Exclude Specific Extensions

Process the directory but skip all `.mp3` and `.txt` files:

```bash
filenorm . -e .mp3 .txt
```

### Save History Log

Normalize files and save/append a timestamped report to `filenorm_log.txt`:

```bash
filenorm . -s kebab --log
```

### Interactive Mode

Review and confirm each file rename interactively (press **Enter** to accept `Y`):

```bash
filenorm . --interactive -c title
```

## Safety

`filenorm` does not overwrite existing files during renaming. If the target file name already exists, the rename is skipped and an error is reported.

Use `--dry-run` to preview changes before making any modifications:

```bash
filenorm . --dry-run
```

For additional control, use `--interactive` to confirm each rename individually.

## Why `filenorm`?

Messy file names can make scripts, backups, automation, and cross-platform workflows unnecessarily difficult.

`filenorm` provides a simple way to turn inconsistent file names into predictable, cleaner names from the command line.

## License

This project is open-source and available under the [License](LICENSE).
