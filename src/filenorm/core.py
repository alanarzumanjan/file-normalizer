import os
import string as s
import unicodedata
from filenorm.translit import transliterate

def split_filename(filename):
    compound_extensions = [
        # Archive formats
        '.tar.gz.bak', '.tar.gz', '.tar.bz2', '.tar.xz', '.tar.zst', '.tar.lz', '.tar.lzma', '.tar.Z', '.tar.bak',
        # User script formats
        '.user.js', '.meta.js',
        # Test and minified formats
        '.d.ts', '.spec.js', '.test.js', '.spec.ts', '.test.ts', '.min.js', '.min.css',
        # Config formats
        '.config.js', '.config.ts', '.config.json', '.config.yaml', '.config.yml',
        # Backup formats
        '.log.gz', '.bak.gz'
    ]

    compound_extensions.sort(key=len, reverse=True)

    # Check for compound extensions first
    for ext in compound_extensions:
        if filename.lower().endswith(ext):
            name_part = filename[:-len(ext)]
            ext_part = filename[-len(ext):]
            return name_part, ext_part
            
    return os.path.splitext(filename)

def normalize_name(name, separator_style, case_style, prefix="", suffix=""):
    transliterated = transliterate(name)
    normalized = unicodedata.normalize('NFKD', transliterated)

    clean_chars = []
    sep_char = {'snake': '_', 'kebab': '-', 'space': ' '}.get(separator_style, '_')

    # Replace spaces and unsupported with chosen separator
    for char in normalized:
        if char in (' ', '-', '_'):
            clean_chars.append(sep_char)
        else:
            if char.isalnum():
                clean_chars.append(char)
    
    new_name = ''.join(clean_chars)

    # Remove consecutive separators and trim leading/trailing ones
    if sep_char != ' ':
        double_sep = sep_char + sep_char
        while double_sep in new_name:
            new_name = new_name.replace(double_sep, sep_char)
        new_name = new_name.strip(sep_char)
    else:
        while '  ' in new_name:
            new_name = new_name.replace('  ', ' ')
        new_name = new_name.strip()

    # Apply text casing style independently
    if case_style == 'lower':
        new_name = new_name.lower()
    elif case_style == 'upper':
        new_name = new_name.upper()
    elif case_style == 'title':
        if sep_char == ' ':
            new_name = new_name.title()
        else:
            words = new_name.split(sep_char)
            new_name = sep_char.join([w.capitalize() for w in words if w])
    elif case_style == 'capitalize':
        new_name = new_name.capitalize()

    # Add prefix and suffix if provided
    if prefix:
        new_name = prefix + new_name
    if suffix:
        new_name = new_name + suffix

    return new_name