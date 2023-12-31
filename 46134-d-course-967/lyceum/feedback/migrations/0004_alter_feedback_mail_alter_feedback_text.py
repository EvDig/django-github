# Generated by Django 4.2.5 on 2023-11-06 19:41

from django.db import migrations, models

__all__ = []


class Migration(migrations.Migration):
    dependencies = [
        ("feedback", "0003_alter_feedback_mail"),
    ]

    operations = [
        migrations.AlterField(
            model_name="feedback",
            name="mail",
            field=models.EmailField(max_length=150, verbose_name="почта"),
        ),
        migrations.AlterField(
            model_name="feedback",
            name="text",
            field=models.TextField(verbose_name="текст"),
        ),
    ]
