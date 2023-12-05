import sys

from django.contrib.auth.models import User
import django.db.models

import users.managers

__all__ = []


class Profile(django.db.models.Model):
    user = django.db.models.OneToOneField(
        User,
        on_delete=django.db.models.CASCADE,
        related_name="profile",
        related_query_name="profile",
    )
    birthday = django.db.models.DateField(
        blank=True,
        null=True,
        verbose_name="день рождения",
    )
    image = django.db.models.ImageField(
        blank=True,
        null=True,
        upload_to="users/avatars/",
        verbose_name="аватарка",
    )
    coffee_count = django.db.models.PositiveIntegerField(
        default=0,
        verbose_name="выпито кофе",
    )
    block_date = django.db.models.DateTimeField(
        verbose_name="время блокировки",
        blank=True,
        null=True,
    )
    attempts_count = django.db.models.PositiveIntegerField(
        default=0,
        verbose_name="попыток входа",
    )

    class Meta:
        verbose_name = "Дополнительное поле"
        verbose_name_plural = "Дополнительные поля"


class User(User):
    objects = users.managers.UserManager()

    class Meta:
        proxy = True
        verbose_name = "пользователь"
        verbose_name_plural = "пользователи"


if "makemigrations" not in sys.argv and "migrate" not in sys.argv:
    django.contrib.auth.models.User._meta.get_field("email")._unique = True
