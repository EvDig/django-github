import django.core.exceptions
import django.test
import parameterized

import catalog.models

__all__ = []


class ItemValidatorsTests(django.test.TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()

        cls.category = catalog.models.Category.objects.create(
            is_published=True,
            name="Тестовая категория",
            slug="test-category-slug",
            weight=100,
        )
        cls.tag = catalog.models.Tag.objects.create(
            is_published=True,
            name="Тестовый тег",
            slug="test-tag-slug",
        )
        cls.image = catalog.models.ItemMainImage.objects.create()

    @parameterized.parameterized.expand(
        ["Превосходно, описание подходит", "Это описание роскошно"],
    )
    def test_validate_positive(self, arg):
        item_count = catalog.models.Item.objects.count()
        self.item = catalog.models.Item(
            name="Тестовый верный товар",
            category=self.category,
            text=arg,
            mimage=self.image,
        )
        self.item.full_clean()
        self.item.save()
        self.item.tags.add(self.tag)

        self.assertEqual(
            catalog.models.Item.objects.count(),
            item_count + 1,
        )

    @parameterized.parameterized.expand(
        ["o", "описание", "нероскошное такое", "совсем непревосх!одное"],
    )
    def test_validate_negative(self, arg):
        item_count = catalog.models.Item.objects.count()
        with self.assertRaises(django.core.exceptions.ValidationError):
            self.item = catalog.models.Item(
                name="Тестовый провальный товар",
                category=self.category,
                text=arg,
                mimage=self.image,
            )
            self.item.full_clean()
            self.item.save()
            self.item.tags.add(self.tag)

        self.assertEqual(
            catalog.models.Item.objects.count(),
            item_count,
        )
