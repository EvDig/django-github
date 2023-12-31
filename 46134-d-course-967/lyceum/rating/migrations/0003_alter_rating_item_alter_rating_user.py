# Generated by Django 4.2.5 on 2023-11-21 19:07

from django.db import migrations, models
import django.db.models.deletion

__all__ = []


class Migration(migrations.Migration):
    dependencies = [
        (
            "catalog",
            "0013_alter_category_normalized_name_and_more_"
            "squashed_0017_alter_item_date_created_alter"
            "_item_date_updated",
        ),
        (
            "users",
            "0003_profile_attempts_count_squashed_0004_"
            "profile_date_blocked_squashed_0005_rename_date_"
            "blocked_profile_block_date",
        ),
        ("rating", "0002_alter_rating_rating"),
    ]

    operations = [
        migrations.AlterField(
            model_name="rating",
            name="item",
            field=models.ForeignKey(
                default=1,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="rating_item_id",
                related_query_name="rating_item_id",
                to="catalog.item",
                verbose_name="оцененный товар",
            ),
        ),
        migrations.AlterField(
            model_name="rating",
            name="user",
            field=models.ForeignKey(
                default=1,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="rating_user_id",
                related_query_name="rating_user_id",
                to="users.user",
                verbose_name="оценивший пользователь",
            ),
        ),
    ]
