from django.conf import settings
from django.contrib.auth.models import User
from django.core.signing import TimestampSigner
from django.shortcuts import reverse
from django.test import Client, override_settings, TestCase
from freezegun import freeze_time

from users.forms import RegisterForm

__all__ = []


class FormTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.client = Client()
        cls.form = RegisterForm

    def test_form_in_context(self):
        response = self.client.get(reverse("users:signup"))
        self.assertIn("form", response.context)

    def test_form_with_error_mail(self):
        form_data = {
            "email": "не мейл",
        }
        form = RegisterForm(data=form_data)

        self.assertFalse(form.is_valid())
        self.assertFormError(
            form,
            "email",
            ["Введите правильный адрес электронной почты."],
        )

    def test_form_with_error_password_not_same(self):
        form_data = {
            "password1": "1_Dnho25dGG11",
            "password2": "1",
        }
        form = RegisterForm(data=form_data)

        self.assertFalse(form.is_valid())
        self.assertFormError(
            form,
            "password2",
            ["Введенные пароли не совпадают."],
        )

    def test_form_with_error_empty_username(self):
        form_data = {"username": ""}
        form = RegisterForm(data=form_data)

        self.assertFalse(form.is_valid())
        self.assertFormError(
            form,
            "username",
            ["Обязательное поле."],
        )


class RegistrationTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.username = "username"
        cls.email = "test@mail.ru"
        cls.password1 = "1_Dnho25dGG11"
        cls.password2 = "1_Dnho25dGG11"

    def test_register_correct_user(self):
        form_data = {
            "username": self.username,
            "email": self.email,
            "password1": self.password1,
            "password2": self.password2,
        }

        users_count = User.objects.count()

        response = self.client.post(
            reverse("users:signup"),
            data=form_data,
            follow=True,
        )

        self.assertRedirects(response, reverse("users:login"))
        self.assertEqual(User.objects.count(), users_count + 1)
        self.assertTrue(
            User.objects.filter(
                username=self.username,
            ).exists(),
        )


class UserActivationTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.username = "username"
        cls.email = "test@mail.ru"
        cls.password1 = "1_Dnho25dGG11"
        cls.password2 = "1_Dnho25dGG11"
        cls.signer = TimestampSigner()

    @override_settings(DEFAULT_USER_IS_ACTIVE=False)
    def test_register_and_activate_correct_user(self):
        form_data = {
            "username": self.username,
            "email": self.email,
            "password1": self.password1,
            "password2": self.password2,
        }

        users_count = User.objects.count()

        response = self.client.post(
            reverse("users:signup"),
            data=form_data,
            follow=True,
        )

        self.assertRedirects(response, reverse("users:login"))
        self.assertEqual(User.objects.count(), users_count + 1)
        self.assertTrue(
            User.objects.filter(
                username=self.username,
                is_active=False,
            ).exists(),
        )

        signed_username = self.signer.sign(self.username)

        self.client.get(
            reverse(
                "users:activate",
                kwargs={"username": signed_username},
            ),
        )

        self.assertTrue(
            User.objects.filter(
                username=self.username,
                is_active=True,
            ).exists(),
        )

    @override_settings(DEFAULT_USER_IS_ACTIVE=False)
    def test_error_activate_after_12_hours(self):
        form_data = {
            "username": self.username,
            "email": self.email,
            "password1": self.password1,
            "password2": self.password2,
        }

        users_count = User.objects.count()

        response = self.client.post(
            reverse("users:signup"),
            data=form_data,
            follow=True,
        )

        self.assertRedirects(response, reverse("users:login"))
        self.assertEqual(User.objects.count(), users_count + 1)
        self.assertTrue(
            User.objects.filter(
                username=self.username,
                is_active=False,
            ).exists(),
        )

        signed_username = self.signer.sign(self.username)

        with freeze_time("2023-12-25"):
            self.client.get(
                reverse(
                    "users:activate",
                    kwargs={"username": signed_username},
                ),
            )

        self.assertTrue(
            User.objects.filter(
                username=self.username,
                is_active=False,
            ).exists(),
        )


class UserLoginTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.username = "username"
        cls.email = "te-st@yandex.ru"
        cls.email_not_normalized = "Te.St+sdf@ya.ru"
        cls.password = "1_Dnho25dGG1"
        cls.signer = TimestampSigner()

    def test_login_with_username_and_email(self):
        # Создаем пользователя
        form_data = {
            "username": self.username,
            "email": self.email,
            "password1": self.password,
            "password2": self.password,
        }

        self.client.post(
            reverse("users:signup"),
            data=form_data,
        )

        signed_username = self.signer.sign(self.username)

        self.client.get(
            reverse(
                "users:activate",
                kwargs={"username": signed_username},
            ),
        )
        self.assertIn("_auth_user_id", self.client.session)
        self.client.get(reverse("users:logout"))

        # Логинимся
        form_data = {
            "username": self.username,
            "password": self.password,
        }

        self.client.post(
            reverse("users:login"),
            data=form_data,
        )

        self.assertIn("_auth_user_id", self.client.session)
        self.client.get(reverse("users:logout"))

        form_data = {
            "username": self.email,
            "password": self.password,
        }

        self.client.post(
            reverse("users:login"),
            data=form_data,
        )

        self.assertIn("_auth_user_id", self.client.session)
        self.client.get(reverse("users:logout"))

        form_data = {
            "username": self.email_not_normalized,
            "password": self.password,
        }

        self.client.post(
            reverse("users:login"),
            data=form_data,
        )

        self.assertIn("_auth_user_id", self.client.session)
        self.client.get(reverse("users:logout"))

        # Блокируем и восстанавливаем пользователя

        form_data = {
            "username": self.email,
            "password": self.password + "1",
        }

        for _ in range(settings.MAX_AUTH_ATTEMPTS):
            self.client.post(
                reverse("users:login"),
                data=form_data,
            )

        self.assertTrue(
            User.objects.filter(
                username=self.username,
                is_active=False,
            ).exists(),
        )

        signed_username = self.signer.sign(self.username)

        self.client.get(
            reverse(
                "users:activate_again",
                kwargs={"username": signed_username},
            ),
        )

        self.assertIn("_auth_user_id", self.client.session)

        self.assertTrue(
            User.objects.filter(
                username=self.username,
                is_active=True,
            ).exists(),
        )

        self.client.get(reverse("users:logout"))

        # Блокируем и (не) восстанавливаем через 7 дней

        form_data = {
            "username": self.email,
            "password": self.password + "1",
        }

        for _ in range(settings.MAX_AUTH_ATTEMPTS):
            self.client.post(
                reverse("users:login"),
                data=form_data,
            )

        self.assertTrue(
            User.objects.filter(
                username=self.username,
                is_active=False,
            ).exists(),
        )

        signed_username = self.signer.sign(self.username)

        with freeze_time("2023-12-25"):
            self.client.get(
                reverse(
                    "users:activate",
                    kwargs={"username": signed_username},
                ),
            )

        self.assertTrue(
            User.objects.filter(
                username=self.username,
                is_active=False,
            ).exists(),
        )

        self.assertNotIn("_auth_user_id", self.client.session)
