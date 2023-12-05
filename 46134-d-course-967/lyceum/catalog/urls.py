from django.urls import path, re_path, register_converter

import catalog.converters
import catalog.views

register_converter(catalog.converters.IntConverter, "integer")

app_name = "catalog"

urlpatterns = [
    path("", catalog.views.item_list, name="item_list"),
    path("new/", catalog.views.new, name="new"),
    path("friday/", catalog.views.friday, name="friday"),
    path("unverified/", catalog.views.unverified, name="unverified"),
    path("<int:pk>/", catalog.views.ItemDetailView.as_view(), name="item"),
    path(
        "converter/<integer:conv_int>/",
        catalog.views.item_convert_re_detail,
        name="item_convert_re_detail",
    ),
    re_path(
        r"re/(?P<conv_int>[0-9]*[1-9]+)/$",
        catalog.views.item_convert_re_detail,
        name="item_convert_re_detail",
    ),
]
