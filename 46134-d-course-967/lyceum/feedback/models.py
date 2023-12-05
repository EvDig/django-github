import django.conf
import django.db.models

__all__ = []


class Feedback(django.db.models.Model):
    STATUS_CHOICES = [
        ("GET", "получено"),
        ("PROCESSING", "в обработке"),
        ("OK", "ответ дан"),
    ]

    text = django.db.models.TextField(
        verbose_name="текст",
    )
    created_on = django.db.models.DateTimeField(
        auto_now_add=True,
    )
    status = django.db.models.CharField(
        verbose_name="статус",
        max_length=11,
        choices=STATUS_CHOICES,
        default="GET",
    )

    class Meta:
        verbose_name = "фидбек"
        verbose_name_plural = "фидбеки"


class PersonalData(django.db.models.Model):
    mail = django.db.models.EmailField(
        max_length=150,
        verbose_name="почта",
    )
    name = django.db.models.CharField(
        max_length=150,
        blank=True,
        null=True,
        verbose_name="имя",
    )

    personal_data = django.db.models.OneToOneField(
        Feedback,
        on_delete=django.db.models.CASCADE,
        related_name="personal_data",
        related_query_name="personal_data",
        verbose_name="личные данные",
        default=1,
    )

    class Meta:
        verbose_name = "личные данные"
        verbose_name_plural = "личные данные"


class StatusLog(django.db.models.Model):
    user = django.db.models.ForeignKey(
        django.conf.settings.AUTH_USER_MODEL,
        on_delete=django.db.models.CASCADE,
    )

    timestamp = django.db.models.DateTimeField(auto_now_add=True)

    feedback = django.db.models.ForeignKey(
        Feedback,
        verbose_name="фидбек",
        on_delete=django.db.models.deletion.CASCADE,
        default=1,
    )

    from_status = django.db.models.CharField(
        db_column="from",
        verbose_name="предыдущий статус",
        max_length=11,
        choices=Feedback.STATUS_CHOICES,
    )

    to = django.db.models.CharField(
        verbose_name="текущий статус",
        max_length=11,
        choices=Feedback.STATUS_CHOICES,
    )


class FeedbackFile(django.db.models.Model):
    def create_path(self, filename):
        return f"uploads/{self.feedback_id}/{filename}"

    file = django.db.models.FileField(
        upload_to=create_path,
        verbose_name="файл",
    )

    feedback = django.db.models.ForeignKey(
        Feedback,
        on_delete=django.db.models.CASCADE,
        related_name="files",
        related_query_name="files",
    )
