import os
import string as s
import unicodedata
from filenorm.translit import transliterate

# Some of the code in this file is adapted from
def split_filename(filename):
    compound_extensions = [
        # Arhive formats
        '.tar.gz', '.tar.bz2', '.tar.xz', '.tar.zst', '.tar.lz', '.tar.lzma', '.tar.Z', '.tar.bak',
        # User script formats
        '.user.js', '.meta.js',
        # Test and minified formats
        '.d.ts', '.spec.js', '.test.js', '.spec.ts', '.test.ts', '.min.js', '.min.css',
        # Config formats
        '.config.js', '.config.ts', '.config.json', '.config.yaml', '.config.yml',
        # Backup formats
        '.log.gz', '.bak.gz', '.tar.gz.bak'
    ]

    compound_extensions.sort(key=len, reverse=True)

    # Check for compound extensions first
    for ext in compound_extensions:
        if filename.lower().endswith(ext):
            name_part = filename[:-len(ext)]
            ext_part = filename[-len(ext):]
            return name_part, ext_part
            
    return os.path.splitext(filename)

# Get allowed characters based on the case style
def get_allowed_chars(case_style):
    if case_style == 'kebab':
        return set(s.ascii_lowercase + s.digits + '-')
    elif case_style == 'snake':
        return set(s.ascii_lowercase + s.digits + '_')
    else:
        return set(s.ascii_lowercase + s.digits + ' _-')

# Normalize based on the case style, allowed characters and prefix/suffix
def normalize_name(name, allowed_chars, case_style, prefix="", suffix=""):
    transliterated = transliterate(name)
    normalized = unicodedata.normalize('NFKD', transliterated)

    clean_chars = []
    separator = '-' if case_style == 'kebab' else '_'

    # Replace spaces and unsupported characters with the operator choice
    for char in normalized:
        if char in (' ', '-', '_'):
            if case_style == 'lower':
                clean_chars.append(' ')
            else:
                clean_chars.append(separator)
        else:
            lower_char = char.lower()
            if lower_char in allowed_chars:
                clean_chars.append(lower_char)
    
    new_name = ''.join(clean_chars)

    # Remove consecutive separators or spaces and trim leading/trailing ones
    if case_style != 'lower':
        double_sep = separator + separator

        while double_sep in new_name: # Remove consecutive separators
            new_name = new_name.replace(double_sep, separator)

        new_name = new_name.strip(separator)
    else:
        while '  ' in new_name:
            new_name = new_name.replace('  ', ' ')
        new_name = new_name.strip()

    # Add prefix and suffix if provided
    if prefix:
        new_name = prefix + new_name
    if suffix:
        new_name = new_name + suffix

    return new_name