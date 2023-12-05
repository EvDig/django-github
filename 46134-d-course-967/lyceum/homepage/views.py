from http import HTTPStatus

from django.http import HttpResponse
from django.shortcuts import render

import catalog.models
from homepage.forms import EchoForm

__all__ = []


def home(request):
    template = "homepage/main.html"
    items = catalog.models.Item.objects.on_main()
    context = {"items": items}
    return render(request, template, context)


def coffee(request):
    if request.user.is_authenticated:
        request.user.profile.coffee_count += 1
        request.user.profile.save()
    return HttpResponse("Я чайник", status=HTTPStatus.IM_A_TEAPOT)


def echo(request):
    if request.method == "POST":
        return HttpResponse(status=HTTPStatus.METHOD_NOT_ALLOWED)
    template = "homepage/echo.html"
    form = EchoForm(request.POST or None)

    context = {
        "form": form,
    }
    return render(request, template, context)


def echo_submit(request):
    if request.method == "POST":
        form = EchoForm(request.POST)
        if form.is_valid():
            text = form.cleaned_data["text"]
            return HttpResponse(f"{text}")
    else:
        return HttpResponse(status=HTTPStatus.METHOD_NOT_ALLOWED)
    return None
