from unidecode import unidecode # type: ignore

def transliterate(text: str) -> str:
    return unidecode(text)