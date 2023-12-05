import django.db.models

__all__ = []


class StatisticsManager(django.db.models.Manager):
    def best_to_worst(self, pk):
        return (
            self.get_queryset()
            .filter(user_id=pk)
            .order_by("-rating", "-last_change")
        )

    def worst_to_best(self, pk):
        return (
            self.get_queryset()
            .filter(user_id=pk)
            .order_by("rating", "-last_change")
        )

    def evaluated_items(self, pk):
        return (
            self.get_queryset()
            .filter(user_id=pk)
            .order_by(
                "-rating",
            )
        )
