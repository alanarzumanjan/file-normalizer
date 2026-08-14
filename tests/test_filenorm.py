import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))

import pytest
from filenorm.core import normalize_name, split_filename

@pytest.mark.parametrize(
    "filename, case_style, separator_style, prefix, suffix, expected",
    [
        # Base case: simple filename with extension
        ("My Cool File.TXT", "lower", "snake", "", "", "my_cool_file.txt"),
        
        # Test with different cases and separators
        ("hello world.png", "upper", "snake", "", "", "HELLO_WORLD.png"),
        ("hello world.png", "title", "kebab", "", "", "Hello-World.png"),
        ("hello world.png", "capitalize", "space", "", "", "Hello world.png"),
        
        # Test with different separators and compound extensions
        ("Archive File.tar.gz", "lower", "snake", "", "", "archive_file.tar.gz"),
        ("Script User.JS", "lower", "kebab", "", "", "script-user.js"),
        
        # Prefix and suffix tests
        ("document.pdf", "lower", "snake", "2026-", "-v1", "2026-document-v1.pdf"),
        
        # Test with non-ASCII characters
        ("Привет Миr.txt", "lower", "snake", "", "", "privet_mir.txt"),
    ],
)
def test_normalize_filename(filename, case_style, separator_style, prefix, suffix, expected):
    name, ext = split_filename(filename)
    new_name = normalize_name(
        name, 
        separator_style=separator_style, 
        case_style=case_style, 
        prefix=prefix, 
        suffix=suffix
    )
    new_ext = ext.replace(' ', '_').lower()
    result = new_name + new_ext
    assert result == expected