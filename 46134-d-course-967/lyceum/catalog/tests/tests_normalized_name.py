import django.core.exceptions
import django.test
import parameterized

import catalog.models
from catalog.text_normalizer import normalize_text

__all__ = []


class NormalizedNameTests(django.test.TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.slug = "test-slug"
        cls.weight = 100

    @parameterized.parameterized.expand(["тег5655", "Тег один миллион"])
    def test_tag_creation_positive(self, arg):
        tag_count = catalog.models.Tag.objects.count()
        self.tag = catalog.models.Tag(
            is_published=True,
            name=arg,
            slug=self.slug,
        )
        self.tag.full_clean()
        self.tag.save()

        self.assertEqual(
            catalog.models.Tag.objects.count(),
            tag_count + 1,
        )

    @parameterized.parameterized.expand(
        ["категория5655", "Категория один миллион"],
    )
    def test_category_creation_positive(self, arg):
        category_count = catalog.models.Category.objects.count()
        self.category = catalog.models.Category(
            is_published=True,
            name=arg,
            slug=self.slug,
            weight=self.weight,
        )
        self.category.full_clean()
        self.category.save()

        self.assertEqual(
            catalog.models.Category.objects.count(),
            category_count + 1,
        )

    @parameterized.parameterized.expand(["тег5655", "Тег Один Миллион"])
    def test_tag_creation_negative(self, arg):
        self.tag = catalog.models.Tag(
            is_published=True,
            name=arg,
            slug=self.slug,
        )
        self.tag.full_clean()
        self.tag.save()
        tag_count = catalog.models.Tag.objects.count()

        with self.assertRaises(django.core.exceptions.ValidationError):
            self.tag = catalog.models.Tag(
                is_published=True,
                name=normalize_text(arg),
                slug=self.slug + "1",
            )
            self.tag.full_clean()
            self.tag.save()

        self.assertEqual(
            catalog.models.Tag.objects.count(),
            tag_count,
        )

    @parameterized.parameterized.expand(
        ["категория5655", "Категория Один Миллион"],
    )
    def test_category_creation_negative(self, arg):
        self.category = catalog.models.Category(
            is_published=True,
            name=arg,
            slug=self.slug,
            weight=self.weight,
        )
        self.category.full_clean()
        self.category.save()
        category_count = catalog.models.Category.objects.count()

        with self.assertRaises(django.core.exceptions.ValidationError):
            self.category = catalog.models.Category(
                is_published=True,
                name=normalize_text(arg),
                slug=self.slug + "1",
                weight=self.weight,
            )
            self.category.full_clean()
            self.category.save()

        self.assertEqual(
            catalog.models.Category.objects.count(),
            category_count,
        )
