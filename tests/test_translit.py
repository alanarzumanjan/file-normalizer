import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))

from filenorm.translit import transliterate


def test_transliterate_cyrillic():
    assert transliterate("Привет мир") == "Privet mir"


def test_transliterate_mixed_text():
    assert transliterate("Привет World") == "Privet World"


def test_transliterate_latin_text():
    assert transliterate("Hello World") == "Hello World"


def test_transliterate_empty_string():
    assert transliterate("") == ""