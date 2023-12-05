import datetime

import django.core.validators
import django.db.models
from django.shortcuts import get_object_or_404
import django.utils.safestring
import django.utils.timezone
from sorl.thumbnail import get_thumbnail
import tinymce.models

import catalog.managers
from catalog.validators import (
    custom_validator,
    ValidateMustContain,
)
from core.models import ModelWithNormalizedName


__all__ = []


class Tag(ModelWithNormalizedName):
    name = django.db.models.CharField(
        max_length=150,
        verbose_name="название",
        default="",
        unique=True,
        help_text="имя",
    )
    slug = django.db.models.SlugField(
        verbose_name="слаг",
        help_text="Отображаемое название",
        unique=True,
        validators=[
            django.core.validators.MaxLengthValidator(200),
        ],
    )

    class Meta:
        verbose_name = "тег"
        verbose_name_plural = "теги"

    def __str__(self):
        return self.name


class Category(ModelWithNormalizedName):
    slug = django.db.models.SlugField(
        verbose_name="слаг",
        help_text="Отображаемое название",
        unique=True,
        validators=[
            django.core.validators.MaxLengthValidator(200),
        ],
    )
    weight = django.db.models.SmallIntegerField(
        verbose_name="вес",
        default=100,
        validators=[
            django.core.validators.MinValueValidator(1),
            django.core.validators.MaxValueValidator(32767),
        ],
    )

    class Meta:
        verbose_name = "категория"
        verbose_name_plural = "категории"

    def __str__(self):
        return self.name


# ЭТОТ МЕНЕДЖЕР НИКАК НЕ ИСПОЛЬЗУЕТСЯ. ЛМС НЕ ВИДИТ ЕГО ЕСЛИ ОН В managers.py
class ItemManager(django.db.models.Manager):
    def on_main(self):
        return (
            self.get_queryset()
            .filter(
                is_published=True,
                is_on_main=True,
                category__is_published=True,
            )
            .select_related("category")
            .order_by("name")
            .prefetch_related(
                django.db.models.Prefetch(
                    "tags",
                    queryset=catalog.models.Tag.objects.filter(
                        is_published=True,
                    ).only(
                        "name",
                    ),
                ),
            )
            .only("name", "category", "text")
        )

    def published(self):
        return (
            self.get_queryset()
            .filter(is_published=True, category__is_published=True)
            .select_related("category")
            .order_by("category__name")
            .prefetch_related(
                django.db.models.Prefetch(
                    "tags",
                    queryset=catalog.models.Tag.objects.filter(
                        is_published=True,
                    ).only(
                        "name",
                    ),
                ),
            )
            .only("name", "category__name", "text")
        )

    def new(self):
        return (
            self.published()
            .filter(
                date_created__gte=django.utils.timezone.now()
                - datetime.timedelta(days=7),
            )
            .order_by("?")[:5]
        )

    def friday(self):
        return (
            self.published()
            .filter(
                date_updated__week_day=6,
            )
            .order_by("date_updated")[:5]
        )

    def unverified(self):
        return self.published().filter(
            date_updated=django.db.models.F("date_created"),
        )

    def item_detail(self, pk):
        return get_object_or_404(
            self.get_queryset()
            .filter(is_published=True, category__is_published=True, id=pk)
            .select_related("mimage", "category")
            .prefetch_related(
                django.db.models.Prefetch(
                    "tags",
                    queryset=catalog.models.Tag.objects.filter(
                        is_published=True,
                    ).only(
                        "name",
                    ),
                ),
            )
            .prefetch_related(
                django.db.models.Prefetch(
                    "images",
                    queryset=catalog.models.ItemImageGallery.objects.only(
                        "image_gallery",
                    ),
                ),
            )
            .only("name", "text", "category"),
        )


class Item(ModelWithNormalizedName):
    objects = catalog.managers.ItemManager()

    text = tinymce.models.HTMLField(
        help_text=(
            "Опишите объект, описание должно содержать"
            " слово 'роскошно' или 'превосходно'"
        ),
        validators=[
            django.core.validators.MinLengthValidator(2),
            custom_validator,
            ValidateMustContain("превосходно", "роскошно"),
        ],
        default="",
        verbose_name="текст",
    )

    tags = django.db.models.ManyToManyField(
        Tag,
        verbose_name="теги",
        blank=True,
    )
    category = django.db.models.ForeignKey(
        Category,
        verbose_name="категория",
        on_delete=django.db.models.deletion.CASCADE,
    )

    is_on_main = django.db.models.BooleanField(
        verbose_name="На главной",
        default=False,
        help_text="состояние видимости с главной страницы",
    )

    date_created = django.db.models.DateTimeField(auto_now_add=True, null=True)
    date_updated = django.db.models.DateTimeField(auto_now=True, null=True)

    class Meta:
        verbose_name = "товар"
        verbose_name_plural = "товары"

    def __str__(self):
        return self.name


class ItemMainImage(django.db.models.Model):
    image = django.db.models.ImageField(
        verbose_name="главное изображение",
        help_text="Выберите главное изображение",
        upload_to="catalog/images/main_item_images/%Y.%m.%d",
        default="Дефолт значение",
    )

    main_image = django.db.models.OneToOneField(
        Item,
        verbose_name="главное изображение",
        related_name="main_image",
        on_delete=django.db.models.deletion.CASCADE,
        blank=True,
        null=True,
        related_query_name="mimage",
    )

    def get_image_300x300(self):
        return get_thumbnail(self.image, "300x300", crop="center", quality=51)

    def image_tmb(
        self,
    ):  # Вызывается напрямую только в админке главных изображений
        if self.image:
            return django.utils.safestring.mark_safe(
                f"<img src='{self.get_image_300x300().url}'>",
            )
        return "Нет изображения"

    def preview(self):  # Когда вызывается для объекта Item
        return self.main_image.image_tmb()

    image_tmb.short_description = "превью"
    image_tmb.allow_tags = True

    class Meta:
        verbose_name = "главное изображение"
        verbose_name_plural = "главные изображения"


class ItemImageGallery(django.db.models.Model):
    image_gallery = django.db.models.ImageField(
        verbose_name="вторичное изображение",
        help_text="Выберите дополнительное изображение",
        upload_to="catalog/images/secondary_item_images/%Y.%m.%d",
        blank=True,
        null=True,
    )

    images_table = django.db.models.ForeignKey(
        Item,
        related_name="images",
        verbose_name="товар",
        on_delete=django.db.models.deletion.CASCADE,
    )

    class Meta:
        verbose_name = "вторичное изображение"
        verbose_name_plural = "вторичные изображения"
