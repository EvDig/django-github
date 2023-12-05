import re

from transliterate import translit

__all__ = []


def normalize_text(value):
    value = re.sub(r"\W", "", value.lower())
    return translit(value, "ru", reversed=True)
