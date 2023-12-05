from django.apps import AppConfig

__all__ = ["StatisticConfig"]


class StatisticConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "statistic"
    verbose_name = "статистика"
