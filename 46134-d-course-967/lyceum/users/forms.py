from django.contrib.auth.forms import UserChangeForm, UserCreationForm
from django.contrib.auth.models import User
import django.forms

import users.models

__all__ = []


class RegisterForm(UserCreationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.visible_fields():
            field.field.widget.attrs["class"] = "form-control"
        self.fields[User.email.field.name].required = True

    class Meta(UserCreationForm.Meta):
        model = User
        fields = [
            User.username.field.name,
            User.email.field.name,
            "password1",
            "password2",
        ]


class ProfileChangeForm(django.forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.visible_fields():
            field.field.widget.attrs["class"] = "form-control"
        self.fields["image"].widget.attrs["type"] = "file"
        self.fields["coffee_count"].required = False
        self.fields["coffee_count"].widget.attrs["disabled"] = True

    class Meta:
        model = users.models.Profile
        fields = (
            users.models.Profile.birthday.field.name,
            users.models.Profile.image.field.name,
            users.models.Profile.coffee_count.field.name,
        )


class UserChangeForm(UserChangeForm):
    password = None

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.visible_fields():
            field.field.widget.attrs["class"] = "form-control"

    class Meta(UserChangeForm.Meta):
        model = User
        fields = [
            User.username.field.name,
            User.email.field.name,
        ]
