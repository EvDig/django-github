import django.core.exceptions
import django.test
from django.test import Client
from django.urls import reverse
import parameterized

import catalog.models

__all__ = []


class ContextTests(django.test.TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.main_image = catalog.models.ItemMainImage.objects.create()
        cls.published_category = catalog.models.Category(
            is_published=True,
            name="Опубликованная категория",
            slug="public_cat",
            weight=50,
        )
        cls.unpublished_category = catalog.models.Category(
            is_published=False,
            name="Неопубликованная категория",
            slug="unpublic_cat",
            weight=50,
        )
        cls.published_tag = catalog.models.Tag(
            is_published=True,
            name="Опубликованный тег",
            slug="published_slug",
        )
        cls.unpublished_tag = catalog.models.Tag(
            is_published=False,
            name="Неопубликованный тег",
            slug="unpublished_slug",
        )
        cls.unpublished_item = catalog.models.Item(
            name="Неопубликованный товар",
            category=cls.published_category,
            text="превосходно",
            is_published=False,
            is_on_main=True,
        )
        cls.published_item = catalog.models.Item(
            name="Опубликованный товар",
            category=cls.published_category,
            text="превосходно",
            is_published=True,
            is_on_main=True,
        )

        cls.published_category.save()
        cls.unpublished_category.save()

        cls.published_tag.save()
        cls.unpublished_tag.save()

        cls.unpublished_item.clean()
        cls.unpublished_item.save()

        cls.published_item.clean()
        cls.published_item.save()

        cls.published_item.tags.add(cls.published_tag.pk)
        cls.published_item.tags.add(cls.unpublished_tag.pk)

    def test_homepage_show_correct_context(self):
        response = django.test.Client().get(reverse("homepage:home"))
        self.assertIn("items", response.context)

    def test_catalog_show_correct_context(self):
        response = django.test.Client().get(reverse("catalog:item_list"))
        self.assertIn("items", response.context)

    def test_homepage_items_count(self):
        response = django.test.Client().get(reverse("homepage:home"))
        items = response.context["items"]
        self.assertEqual(len(items), 1)

    def test_context_type_test(self):
        response = django.test.Client().get(reverse("homepage:home"))
        items = response.context["items"]
        self.assertIsInstance(items[0], catalog.models.Item)

    @parameterized.parameterized.expand(
        [
            "is_published",
            "main_image",
        ],
    )
    def test_not_in_published(self, arg):
        response = Client().get(reverse("catalog:item_list"))
        item = response.context["items"][0]
        self.assertEqual(len(response.context["items"]), 1)
        self.assertNotIn(arg, item.__dict__)

    @parameterized.parameterized.expand(
        [
            "name",
            "text",
            "category_id",
            "_prefetched_objects_cache",
        ],
    )
    def test_in_published(self, arg):
        response = Client().get(reverse("catalog:item_list"))
        item = response.context["items"][0]
        self.assertEqual(len(response.context["items"]), 1)
        self.assertIn(arg, item.__dict__)
