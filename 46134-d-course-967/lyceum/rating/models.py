import django.db.models

import catalog.models
import statistic.managers
import users.models

__all__ = []


class Rating(django.db.models.Model):
    objects = statistic.managers.StatisticsManager()

    RATING_CHOICES = [
        (1, "Ненависть"),
        (2, "Неприязнь"),
        (3, "Нейтрально"),
        (4, "Обожание"),
        (5, "Любовь"),
    ]

    rating = django.db.models.PositiveIntegerField(
        verbose_name="оценка",
        choices=RATING_CHOICES,
        blank=True,
        null=True,
    )

    last_change = django.db.models.DateTimeField(
        auto_now=True,
    )

    user = django.db.models.ForeignKey(
        users.models.User,
        on_delete=django.db.models.CASCADE,
        related_name="rating_user_id",
        related_query_name="rating_user_id",
        verbose_name="оценивший пользователь",
        default=1,
    )

    item = django.db.models.ForeignKey(
        catalog.models.Item,
        on_delete=django.db.models.CASCADE,
        related_name="rating_item_id",
        related_query_name="rating_item_id",
        verbose_name="оцененный товар",
        default=1,
    )

    class Meta:
        verbose_name = "оценка"
        verbose_name_plural = "оценки"
