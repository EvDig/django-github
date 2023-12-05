from django.db.models import Avg
from django.http import (
    HttpResponse,
    HttpResponseForbidden,
    HttpResponseRedirect,
)
from django.shortcuts import render, reverse
import django.views

import catalog.models
import rating.forms
import rating.models

__all__ = []


def item_list(request):
    template = "catalog/item_list.html"
    items = catalog.models.Item.objects.published()
    context = {"items": items}
    return render(request, template, context)


def new(request):
    template = "catalog/item_list.html"
    items = catalog.models.Item.objects.new()
    context = {"items": items}
    return render(request, template, context)


def friday(request):
    template = "catalog/item_list.html"
    items = catalog.models.Item.objects.friday()
    context = {"items": items}
    return render(request, template, context)


def unverified(request):
    template = "catalog/item_list.html"
    items = catalog.models.Item.objects.unverified()
    context = {"items": items}
    return render(request, template, context)


class ItemDetailView(
    django.views.generic.DetailView,
    django.views.generic.edit.ModelFormMixin,
):
    template = "catalog/item_detail.html"
    model = catalog.models.Item
    form_class = rating.forms.RatingForm

    def get_success_url(self):
        return reverse("catalog:item", kwargs={"pk": self.object.pk})

    def post(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return HttpResponseForbidden()
        self.object = self.get_object()
        rating_form = self.get_form(self.form_class)
        if rating_form.is_valid():
            obj, created = rating.models.Rating.objects.update_or_create(
                item_id=self.object.id,
                user_id=self.request.user.id,
            )
            obj.rating = rating_form.cleaned_data["rating"]
            if not obj.rating:
                obj.delete()
            else:
                obj.save()
            return HttpResponseRedirect(self.get_success_url())
        return self.form_invalid(rating_form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        average_rating = (
            rating.models.Rating.objects.filter(
                item_id=self.object.id,
            ).aggregate(Avg("rating"))["rating__avg"]
            or 0
        )
        rating_count = rating.models.Rating.objects.filter(
            item_id=self.object.id,
        ).count()
        context["avg_rating"] = round(average_rating, 2)
        context["rating_count"] = rating_count
        if self.request.user.is_authenticated:
            try:
                context["form"] = self.form_class(
                    instance=rating.models.Rating.objects.get(
                        item_id=self.object.id,
                        user_id=self.request.user.id,
                    ),
                )
            except rating.models.Rating.DoesNotExist:
                pass
        return context


def item_convert_re_detail(request, conv_int):
    return HttpResponse(f"{int(conv_int)}")
