# File Normalizer (`filenorm`)

A lightweight, cross-platform command-line utility for cleaning up and normalizing file names.

`filenorm` standardizes file names by configuring case styles, word separators, adding custom prefixes/suffixes, transliterating characters, and keeping complex extensions safe.

## Features

- **Flexible Case Styles (`-c`,`--case`)** — choose between `lower`, `upper`, `title` (Each Word Capitalized), or `capitalize`.
- **Word Separators (`-s`,`--separator`)** — choose how to separate words: `snake` (underscores), `kebab` (hyphens), or `space`.
- **Prefixes & Suffixes (`-p`,`-x`,`--pref`,`--suf`,`--prefix`, `--suffix`)** — add a fixed text at the beginning or end of each file (suffixes are smartly placed before the extension).
- **Smart Extension Protection** — ensures transformations apply only to the file name while keeping complex/compound extensions (like `.tar.gz`, `.user.js`, `.d.ts`) safe and untouched.
- **Transliteration** — automatically converts non-Latin characters (like Cyrillic, Chinese, etc.) into standard Latin script using `unidecode`.
- **Special character removal** — removes unsupported or disruptive characters.
- **Recursive mode (`-r`)** — processes files inside nested directories.
- **Dry-run mode (`-d`)** — previews changes without renaming anything.
- **Windows installation (`-i`,`--install`)** — automatically copies the executable and adds it to the user's PATH environment variable.

## Installation

### Option 1: Install with `pip` — (Recommended for all systems)

**[Download Python](https://www.python.org/downloads/)** + add to Environment Variables Path.

If you have Python and `pip` installed, you can install `filenorm` globally in an isolated environment:

**Check downloads**

```bash
python --version
pip --version
```

**Install**

```bash
pip install git+https://github.com/alanarzumanjan/file-normalizer.git
```

### Option 2: Standalone binaries

No Python installation is required when using the pre-compiled binaries.

Download the latest release from the [GitHub Releases](https://github.com/alanarzumanjan/file-normalizer/releases) page.

Available binaries:

- **Linux:** `filenorm-linux-amd64`
- **MacOS:** `filenorm-macos-universal`

For macOS & Linux:
Download the binary and the install.sh script into the same folder, open your terminal there, and run:

```bash
bash install.sh
```

- **Windows:** `filenorm-windows-amd64.exe`

For Windows:
Open a `Downloads directory` - `cd $HOME\Downloads` in PowerShell and write:

```powershell
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
| `-s`, `--separator {snake,kebab,space}` | Word separator style (default: snake) |
| `-p`,`--pref`, `--prefix TEXT` | Add a fixed prefix to file names. |
| `-x`,`--suf`,`--suffix TEXT` | Add a fixed suffix to file names (before extension). |
| `-i`, `--install` | automatically copies the executable and adds it to the user's PATH environment variable(Windows) |

## Examples

### Preview changes

Preview the changes that would be made in the current directory without modifying any files:

```bash
filenorm --dry-run
```

### Normalize recursively

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

### All Combination

```bash
filenorm /path/to/your/files --recursive --case title --separator kebab --prefix "project-" --suffix "-v1" --dry-run
```

or Shortened Command Version

```bash
filenorm /path/to/your/files -r -d -c title -s kebab -p "project-" -x "-v1"
```

Current Directory Target

```bash
filenorm . 
```

### Rebuild config

**Rebuild in `root repo directory`**

```bash
pip uninstall -e .
pip install -e .
```

## Why `filenorm`?

Messy file names can make scripts, backups, automation, and cross-platform workflows unnecessarily difficult.

`filenorm` provides a simple way to turn inconsistent file names into predictable, cleaner names from the command line.

## License

This project is open-source and available under the [License](LICENSE).
