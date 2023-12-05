# Generated by Django 4.2.5 on 2023-11-06 19:10

from django.db import migrations, models

__all__ = []


class Migration(migrations.Migration):
    dependencies = [
        ("feedback", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="feedback",
            name="mail",
            field=models.EmailField(
                help_text="ваша почта",
                max_length=150,
                verbose_name="почта",
            ),
        ),
    ]