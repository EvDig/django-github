import django.contrib.auth.decorators
from django.db.models import Avg
import django.views

import catalog.models
import rating.forms
import rating.models
import users.models

__all__ = []


class EvaluatedItems(django.views.generic.ListView):
    template_name = "statistic/evaluated_items.html"
    model = catalog.models.Item

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        eval_items_id = list(
            rating.models.Rating.objects.evaluated_items(
                self.request.user.id,
            ).values_list("item_id", flat=True),
        )

        context["eval_items"] = (
            self.model.objects.filter(
                id__in=eval_items_id,
            )
            .order_by("-rating_item_id__rating")
            .filter(rating_item_id__user_id=self.request.user.id)
        )
        return context


class ItemStatDetail(django.views.generic.TemplateView):
    template_name = "statistic/item_stat_detail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        ratings = list(
            rating.models.Rating.objects.filter(
                item_id=kwargs.get("pk"),
            ).values_list("rating", flat=True),
        )
        if ratings:
            rating_min = rating.models.Rating.objects.filter(
                rating=min(ratings),
            ).order_by("-last_change")[0]

            rating_max = rating.models.Rating.objects.filter(
                rating=max(ratings),
            ).order_by("-last_change")[0]

            average_rating = round(sum(ratings) / len(ratings), 2)
            context["avg_rating"] = average_rating
            context["ratings_count"] = len(ratings)
            context["best_and_worst_rating_user"] = [
                users.models.User.objects.get(id=rating_max.user_id),
                users.models.User.objects.get(id=rating_min.user_id),
            ]
        try:
            context["item_name"] = catalog.models.Item.objects.get(
                id=kwargs.get("pk"),
            ).name
            context["item_id"] = catalog.models.Item.objects.get(
                id=kwargs.get("pk"),
            ).id
        except catalog.models.Item.DoesNotExist:
            context["item_name"] = None
        return context


class StatisticDetail(django.views.generic.TemplateView):
    template_name = "statistic/statistic_detail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        ratings = rating.models.Rating.objects.best_to_worst(
            self.request.user.id,
        )
        worst_to_best_ratings = rating.models.Rating.objects.worst_to_best(
            self.request.user.id,
        )
        average_rating = round(
            ratings.aggregate(Avg("rating"))["rating__avg"] or 0,
            2,
        )
        try:
            context["best_rating"] = ratings[0].rating
            context["best_and_worst_rating_items"] = [
                catalog.models.Item.objects.get(id=ratings[0].item_id),
                catalog.models.Item.objects.get(
                    id=worst_to_best_ratings[0].item_id,
                ),
            ]
            context["worst_rating"] = worst_to_best_ratings[0].rating
        except IndexError:
            context["best_and_worst_rating_items"] = []
        context["avg_rating"] = average_rating
        context["ratings_count"] = len(ratings)
        return context
