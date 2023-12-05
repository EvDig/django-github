from http import HTTPStatus

from django.core.signing import TimestampSigner
import django.test
from django.test import Client
from django.urls import reverse
import parameterized

import catalog.models
import rating.forms
import rating.models

__all__ = []


class ItemRatingTests(django.test.TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.username = "username"
        cls.email = "test@mail.ru"
        cls.password1 = "1_Dnho25dGG11"
        cls.password2 = "1_Dnho25dGG11"
        cls.signer = TimestampSigner()
        cls.client = Client()
        cls.form = rating.forms.RatingForm()
        cls.category = catalog.models.Category.objects.create(
            is_published=True,
            name="категория1",
            slug="cat1",
            weight=50,
        )
        cls.item = catalog.models.Item.objects.create(
            name="тестовый товар",
            category=cls.category,
            text="превосходно",
            is_published=True,
            is_on_main=False,
        )

    @parameterized.parameterized.expand([1, 2, 3, 4, 5])
    def test_post_valid_rating(self, arg):
        form_data = {
            "username": self.username,
            "email": self.email,
            "password1": self.password1,
            "password2": self.password2,
        }

        self.client.post(
            reverse("users:signup"),
            data=form_data,
            follow=True,
        )

        signed_username = self.signer.sign(self.username)

        self.client.get(
            reverse(
                "users:activate",
                kwargs={"username": signed_username},
            ),
        )

        form_data = {
            "username": self.username,
            "password": self.password1,
        }

        self.client.post(
            reverse("users:login"),
            data=form_data,
        )

        self.assertIn("_auth_user_id", self.client.session)

        form_data = {
            "rating": arg,
        }

        self.form.data = form_data

        rating_count = rating.models.Rating.objects.count()

        response = self.client.post(
            reverse("catalog:item", kwargs={"pk": self.item.id}),
            data=form_data,
            follow=True,
        )

        self.assertRedirects(
            response,
            reverse("catalog:item", kwargs={"pk": self.item.id}),
        )
        self.assertEqual(
            rating.models.Rating.objects.count(),
            rating_count + 1,
        )

    def test_post_empty_rating(self):
        form_data = {
            "username": self.username,
            "email": self.email,
            "password1": self.password1,
            "password2": self.password2,
        }

        self.client.post(
            reverse("users:signup"),
            data=form_data,
            follow=True,
        )

        signed_username = self.signer.sign(self.username)

        self.client.get(
            reverse(
                "users:activate",
                kwargs={"username": signed_username},
            ),
        )

        form_data = {
            "username": self.username,
            "password": self.password1,
        }

        self.client.post(
            reverse("users:login"),
            data=form_data,
        )

        self.assertIn("_auth_user_id", self.client.session)

        form_data = {
            "rating": "",
        }

        self.form.data = form_data

        rating_count = rating.models.Rating.objects.count()

        response = self.client.post(
            reverse("catalog:item", kwargs={"pk": self.item.id}),
            data=form_data,
            follow=True,
        )

        self.assertRedirects(
            response,
            reverse("catalog:item", kwargs={"pk": self.item.id}),
        )
        self.assertEqual(
            rating.models.Rating.objects.count(),
            rating_count,
        )

    @parameterized.parameterized.expand([1, 2, 3, 4, 5])
    def test_post_valid_rating_while_anonymous(self, arg):
        form_data = {
            "rating": arg,
        }

        self.form.data = form_data

        rating_count = rating.models.Rating.objects.count()

        response = self.client.post(
            reverse("catalog:item", kwargs={"pk": self.item.id}),
            data=form_data,
            follow=True,
        )

        self.assertEqual(response.status_code, HTTPStatus.FORBIDDEN)
        self.assertEqual(
            rating.models.Rating.objects.count(),
            rating_count,
        )
