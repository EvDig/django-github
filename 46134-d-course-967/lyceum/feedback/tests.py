import tempfile

from django.core.files.uploadedfile import SimpleUploadedFile
from django.shortcuts import reverse
from django.test import Client, override_settings, TestCase

from feedback.forms import FeedbackForm, PersonalDataForm
from feedback.models import Feedback, FeedbackFile


__all__ = []


class FormTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.client = Client()
        cls.form = FeedbackForm()
        cls.form_2 = PersonalDataForm()

    def test_labels(self):
        text_label = FormTests.form.fields["text"].label
        mail_label = FormTests.form_2.fields["mail"].label
        self.assertEqual(text_label, "Текст отзыва")
        self.assertEqual(mail_label, "Ваша почта")

    def test_help_texts(self):
        mail_help_text = FormTests.form_2.fields["mail"].help_text
        self.assertEqual(
            mail_help_text,
            "Введите вашу почту в формате example@ex.com",
        )

    def test_form_in_context(self):
        response = self.client.get(reverse("feedback:feedback"))
        self.assertIn("form", response.context)

    def test_redirect_after_submit(self):
        form_data = {"text": "отзыв", "mail": "1@1.ru", "status": "PROCESSING"}
        response = self.client.post(
            reverse("feedback:feedback"),
            data=form_data,
            follow=True,
        )

        self.assertRedirects(response, reverse("feedback:feedback"))

    def test_form_with_error_mail(self):
        form_data = {
            "mail": "не мейл",
        }
        form = PersonalDataForm(data=form_data)

        self.assertFalse(form.is_valid())
        self.assertFormError(
            form,
            "mail",
            ["Введите правильный адрес электронной почты."],
        )

    def test_form_with_error_empty(self):
        form_data = {
            "text": "",
        }
        form_2_data = {"mail": ""}
        form = FeedbackForm(data=form_data)
        form_2 = PersonalDataForm(data=form_2_data)

        self.assertFalse(form.is_valid())
        self.assertFalse(form_2.is_valid())
        self.assertFormError(form, "text", ["Обязательное поле."])
        self.assertFormError(form_2, "mail", ["Обязательное поле."])


class FeedbackCreationTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.name = ""
        cls.text = "текст отзыва"
        cls.mail = "test@mail.ru"

    def test_create_with_valid_form(self):
        form_data = {
            "text": self.text,
            "mail": self.mail,
            "name": self.name,
        }

        feedback_count = Feedback.objects.count()

        response = self.client.post(
            reverse("feedback:feedback"),
            data=form_data,
            follow=True,
        )

        self.assertRedirects(response, reverse("feedback:feedback"))
        self.assertEqual(Feedback.objects.count(), feedback_count + 1)
        self.assertTrue(
            Feedback.objects.filter(
                text=self.text,
            ).exists(),
        )

    @override_settings(
        MEDIA_ROOT=tempfile.TemporaryDirectory(prefix="uploads").name,
    )
    def test_upload_multiple_files(self):
        form_data = {
            "text": self.text,
            "mail": self.mail,
            "name": self.name,
            "files": [
                SimpleUploadedFile("test_txt.txt", b"file_content"),
                SimpleUploadedFile("test_txt2.txt", b"file_content2"),
            ],
        }

        response = self.client.post(
            reverse("feedback:feedback"),
            data=form_data,
            follow=True,
        )

        filename_1 = form_data["files"][0].name
        filename_2 = form_data["files"][1].name
        self.assertRedirects(response, reverse("feedback:feedback"))
        self.assertTrue(
            FeedbackFile.objects.filter(
                file__exact=f"uploads/1/{filename_1}",
            ).exists(),
        )
        self.assertTrue(
            FeedbackFile.objects.filter(
                file__exact=f"uploads/1/{filename_2}",
            ).exists(),
        )
