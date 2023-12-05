import django.core.exceptions
import django.db.models

import catalog.text_normalizer

__all__ = []


class ModelWithNormalizedName(django.db.models.Model):
    name = django.db.models.CharField(
        max_length=150,
        verbose_name="название",
        default="",
        unique=True,
        help_text="имя",
    )
    is_published = django.db.models.BooleanField(
        default=True,
        verbose_name="опубликовано",
        help_text="состояние публикации",
    )
    normalized_name = django.db.models.CharField(
        max_length=150,
        verbose_name="нормализованное имя",
        unique=True,
        editable=False,
        null=True,
    )

    class Meta:
        abstract = True

    def clean(self, *args, **kwargs):
        normalized = catalog.text_normalizer.normalize_text(self.name)
        if (
            self.__class__.objects.filter(normalized_name=normalized)
            .exclude(id=self.id)
            .exists()
        ):
            raise django.core.exceptions.ValidationError(
                f"Нормализованное имя для {self.name} уже существует"
                f" в базе данных: {normalized}",
            )
        super().clean()

    def save(self, *args, **kwargs):
        normalized = catalog.text_normalizer.normalize_text(self.name)
        self.normalized_name = normalized
        return super().save(*args, **kwargs)
