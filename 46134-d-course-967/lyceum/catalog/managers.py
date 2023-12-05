import datetime

import django.core.validators
import django.db.models
from django.shortcuts import get_object_or_404
import django.utils.safestring
import django.utils.timezone

import catalog.models

__all__ = []


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
