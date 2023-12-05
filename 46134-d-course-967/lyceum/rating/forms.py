import django.forms

from rating.models import Rating

__all__ = []


class RatingForm(django.forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.visible_fields():
            field.field.widget.attrs["class"] = "form-control"

    class Meta:
        model = Rating
        fields = [
            "rating",
        ]

        labels = {
            "rating": "Оценка товара",
        }
