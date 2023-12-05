import re

from django.conf import settings

__all__ = []


class Middleware:
    _counter = 0  # считается для всех юсеров

    @classmethod
    def increment_counter(cls):
        cls._counter += 1

    def __init__(self, get_response):
        self.get_response = get_response
        self.content_reversed = ""

    def __call__(self, request):
        response = self.get_response(request)
        if Middleware._counter % 10 == 0 and settings.ALLOW_REVERSE:
            response.content = self.content_reversed
            return response
        return response

    def process_view(self, request, view_func, args, kwargs):
        self.increment_counter()
        if Middleware._counter % 10 == 0 and settings.ALLOW_REVERSE:
            if kwargs:
                content = view_func(request, kwargs).content.decode("utf-8")
            else:
                content = view_func(request).content.decode("utf-8")
            self.content_reversed = self.reverse_russian_words(content)

    def reverse_russian_words(self, text):
        return re.sub(
            r"\b[а-яА-ЯёЁ]+\b",
            lambda x: x.group(0)[::-1],
            text,
        )
