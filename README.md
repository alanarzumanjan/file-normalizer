# File Normalizer (`filenorm`)

A lightweight, cross-platform command-line utility for cleaning up and normalizing file names.

`filenorm` standardizes file names by converting them to lowercase, replacing spaces, and removing unsupported or disruptive characters.

## Features

- **Lowercase conversion** — converts file names to lowercase.
- **Space handling** — replaces spaces with a consistent separator.
- **Special character removal** — removes unsupported or disruptive characters.
- **Recursive mode (`-r`)** — processes files inside nested directories.
- **Dry-run mode (`-d`)** — previews changes without renaming anything.

## Installation

### Option 1: Install with `pipx` — Recommended

If you have Python and `pipx` installed, you can install `filenorm` globally in an isolated environment:

```bash
pipx install git+https://github.com/alanarzumanjan/file-normalizer.git
```

### Option 2: Standalone binaries

No Python installation is required when using the pre-compiled binaries.

Download the latest release from the [GitHub Releases](https://github.com/alanarzumanjan/file-normalizer/releases) page.

Available binaries:

- **Linux:** `filenorm-linux-amd64`
- **Windows:** `filenorm-windows-amd64.exe`

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

## Examples

### Preview changes

Preview the changes that would be made in the current directory without modifying any files:

```bash
filenorm --dry-run
```

### Normalize a specific directory

Normalize files in a specific directory:

```bash
filenorm /path/to/your/music
```

### Normalize recursively

Process files in the target directory and all nested directories:

```bash
filenorm /path/to/your/music --recursive
```

### Combine options

Preview recursive changes without modifying any files:

```bash
filenorm /path/to/your/music --recursive --dry-run
```

## Why `filenorm`?

Messy file names can make scripts, backups, automation, and cross-platform workflows unnecessarily difficult.

`filenorm` provides a simple way to turn inconsistent file names into predictable, cleaner names from the command line.

## License

This project is open-source and available under the [MIT License](LICENSE).
