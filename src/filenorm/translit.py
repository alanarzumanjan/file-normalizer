from unidecode import unidecode

def transliterate(text: str) -> str:
    return unidecode(text)