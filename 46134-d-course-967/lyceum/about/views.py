from django.http import HttpResponse
from django.shortcuts import render

__all__ = []


def description(request):
    template = "about/about.html"
    context = {}
    return render(request, template, context)


def test(request):
    return HttpResponse(
        "Привет, этo почтi-почти Pуcский текст@, просто≈"
        " Как-то со спецü символами:) ¡сорри∑! Hу ещё раз ¡сорри!"
        " Ёжика не видели?",
    )
