from http import HTTPStatus

from django.test import Client, TestCase
from django.test.utils import override_settings
from django.urls import reverse
import parameterized

import catalog.models

__all__ = []


class ContextTests(TestCase):
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

    @parameterized.parameterized.expand(
        [
            "is_published",
            "main_image",
        ],
    )
    def test_not_in_homepage(self, arg):
        response = Client().get(reverse("homepage:home"))
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
    def test_in_homepage(self, arg):
        response = Client().get(reverse("homepage:home"))
        item = response.context["items"][0]
        self.assertEqual(len(response.context["items"]), 1)
        self.assertIn(arg, item.__dict__)


class StaticURLTests(TestCase):
    def test_homepage_endpoint(self):
        right_data = ["/", ""]
        for url in right_data:
            response = Client().get(url)
            self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_coffee_endpoint(self):
        response = Client().get(reverse("homepage:coffee"))
        self.assertEqual(response.status_code, HTTPStatus.IM_A_TEAPOT)
        self.assertEqual(response.content.decode("utf-8"), "Я чайник")

    @override_settings(ALLOW_REVERSE=True)
    def test_reverse_allowed_endpoint(self):
        client = Client()
        client2 = Client()
        for i in range(4):
            response = client.get(reverse("homepage:coffee"))
            if i != 3:
                self.assertEqual(response.content.decode("utf-8"), "Я чайник")
            elif i == 3:
                self.assertEqual(response.content.decode("utf-8"), "Я кинйач")
        for i in range(5):
            response = client.get(reverse("homepage:coffee"))
            self.assertEqual(response.content.decode("utf-8"), "Я чайник")
        for i in range(5):
            response = client2.get(reverse("homepage:coffee"))
            if i != 4:
                self.assertEqual(response.content.decode("utf-8"), "Я чайник")
            elif i == 4:
                self.assertEqual(response.content.decode("utf-8"), "Я кинйач")

    @override_settings(ALLOW_REVERSE=False)
    def test_reverse_forbidden_endpoint(self):
        client = Client()
        for i in range(10):
            response = client.get(reverse("homepage:coffee"))
            self.assertEqual(response.content.decode("utf-8"), "Я чайник")
        for i in range(10):
            response = client.get(
                reverse(
                    "catalog:item_convert_re_detail",
                    kwargs={"conv_int": 1},
                ),
            )
            decoded = response.content.decode("utf-8")
            self.assertEqual(decoded, "1")
