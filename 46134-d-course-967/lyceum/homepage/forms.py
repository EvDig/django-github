import django.forms

__all__ = []


class EchoForm(django.forms.Form):
    text = django.forms.CharField(
        label="Текст для эхо",
    )
