import os
import unicodedata

from filenorm.translit import transliterate
from filenorm.compound_extensions import COMPOUND_EXTENSIONS

def split_filename(filename):
    for ext in COMPOUND_EXTENSIONS:
        if filename.lower().endswith(ext):
            name_part = filename[:-len(ext)]
            ext_part = filename[-len(ext):]
            return name_part, ext_part
            
    return os.path.splitext(filename)

def normalize_name(name, separator_style, case_style, prefix="", suffix=""):
    transliterated = transliterate(name)
    normalized = unicodedata.normalize('NFKD', transliterated)

    clean_chars = []
    sep_char = {
        "snake": "_",
        "kebab": "-",
        "space": " "
    }.get(separator_style, "_")

    for char in normalized:
        if char in (" ", "-", "_"):
            clean_chars.append(sep_char)
        elif char.isalnum():
            clean_chars.append(char)
    
    new_name = "".join(clean_chars)

    if sep_char != " ":
        double_sep = sep_char + sep_char
        while double_sep in new_name:
            new_name = new_name.replace(double_sep, sep_char)
        new_name = new_name.strip(sep_char)
    else:
        while "  " in new_name:
            new_name = new_name.replace("  ", " ")
        new_name = new_name.strip()

    if case_style == "lower":
        new_name = new_name.lower()

    elif case_style == "upper":
        new_name = new_name.upper()

    elif case_style == "title":
        if sep_char == " ":
            new_name = new_name.title()
        else:
            words = new_name.split(sep_char)
            new_name = sep_char.join(
                word.capitalize()
                for word in words
                if word
            )

    elif case_style == "capitalize":
        new_name = new_name.capitalize()

    if prefix:
        new_name = prefix + new_name
    if suffix:
        new_name = new_name + suffix

    return new_name