import re

import django.core.exceptions
import django.core.validators
import django.utils.deconstruct

__all__ = []


def custom_validator(value):
    if not re.search(r"(?:\bроскошно|превосходно)\b", value.lower()):
        raise django.core.exceptions.ValidationError(
            "В тексте должно быть 'превосходно' или 'роскошно'",
        )


@django.utils.deconstruct.deconstructible
class ValidateMustContain(django.core.validators.BaseValidator):
    regex = r"\b(?:{})\b"

    def __init__(self, *words, message=None, code=None):
        self.words = words
        self.regex = ValidateMustContain.regex.format("|".join(words))
        super().__init__(message, code)

    def __call__(self, value):
        if not re.search(self.regex, value, re.IGNORECASE):
            words_join = ", ".join(self.words)
            raise django.core.exceptions.ValidationError(
                (
                    f"{value} не содержит ни одного слова из списка: "
                    f" {words_join}"
                ),
            )

    def __eq__(self, other):
        return self.message == other.message
