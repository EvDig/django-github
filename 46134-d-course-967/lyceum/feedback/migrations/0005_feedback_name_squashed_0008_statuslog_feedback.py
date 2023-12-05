# Generated by Django 4.2.5 on 2023-11-08 17:27

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion

__all__ = []


class Migration(migrations.Migration):
    replaces = [
        ("feedback", "0005_feedback_name"),
        ("feedback", "0006_alter_feedback_options_feedback_status_statuslog"),
        ("feedback", "0007_alter_feedback_name"),
        ("feedback", "0008_statuslog_feedback"),
    ]

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("feedback", "0004_alter_feedback_mail_alter_feedback_text"),
    ]

    operations = [
        migrations.AddField(
            model_name="feedback",
            name="name",
            field=models.CharField(blank=True, max_length=150, null=True),
        ),
        migrations.AlterModelOptions(
            name="feedback",
            options={
                "verbose_name": "фидбек",
                "verbose_name_plural": "фидбеки",
            },
        ),
        migrations.AddField(
            model_name="feedback",
            name="status",
            field=models.CharField(
                choices=[
                    ("GET", "получено"),
                    ("PROCESSING", "в обработке"),
                    ("OK", "ответ дан"),
                ],
                default="PROCESSING",
                max_length=11,
                verbose_name="статус",
            ),
        ),
        migrations.AlterField(
            model_name="feedback",
            name="name",
            field=models.CharField(
                blank=True,
                max_length=150,
                null=True,
                verbose_name="имя",
            ),
        ),
        migrations.CreateModel(
            name="StatusLog",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("timestamp", models.DateTimeField(auto_now_add=True)),
                (
                    "from_status",
                    models.CharField(
                        choices=[
                            ("GET", "получено"),
                            ("PROCESSING", "в обработке"),
                            ("OK", "ответ дан"),
                        ],
                        db_column="from",
                        max_length=11,
                        verbose_name="предыдущий статус",
                    ),
                ),
                (
                    "to",
                    models.CharField(
                        choices=[
                            ("GET", "получено"),
                            ("PROCESSING", "в обработке"),
                            ("OK", "ответ дан"),
                        ],
                        max_length=11,
                        verbose_name="текущий статус",
                    ),
                ),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "feedback",
                    models.ForeignKey(
                        default=1,
                        on_delete=django.db.models.deletion.CASCADE,
                        to="feedback.feedback",
                        verbose_name="фидбек",
                    ),
                ),
            ],
        ),
    ]