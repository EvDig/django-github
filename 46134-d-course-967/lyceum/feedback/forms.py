import django.forms

from feedback.models import Feedback, PersonalData

__all__ = []


class FeedbackForm(django.forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.visible_fields():
            field.field.widget.attrs["class"] = "form-control"

    class Meta:
        model = Feedback
        exclude = ["created_on", "status"]

        labels = {
            "text": "Текст отзыва",
        }


class PersonalDataForm(django.forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.visible_fields():
            field.field.widget.attrs["class"] = "form-control"

    class Meta:
        model = PersonalData
        exclude = ["personal_data"]

        labels = {
            "mail": "Ваша почта",
            "name": "Ваше имя (необ.)",
        }

        help_texts = {"mail": "Введите вашу почту в формате example@ex.com"}


class MultipleFileInput(django.forms.ClearableFileInput):
    allow_multiple_selected = True


class MultipleFileField(django.forms.FileField):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault("widget", MultipleFileInput())
        super().__init__(*args, **kwargs)

    def clean(self, data, initial=None):
        single_file_clean = super().clean
        return (
            [single_file_clean(d, initial) for d in data]
            if isinstance(data, (list, tuple))
            else single_file_clean(data, initial)
        )


class FeedbackFileForm(django.forms.Form):
    files = MultipleFileField(label="Файлы", required=False)
