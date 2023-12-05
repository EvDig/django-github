from django.contrib.auth.decorators import login_required
from django.urls import path

import statistic.views

app_name = "statistic"

urlpatterns = [
    path(
        "",
        login_required(statistic.views.StatisticDetail.as_view()),
        name="user_ratings_detail",
    ),
    path(
        "list/",
        login_required(statistic.views.EvaluatedItems.as_view()),
        name="list",
    ),
    path(
        "detail/<int:pk>",
        statistic.views.ItemStatDetail.as_view(),
        name="rating_detail",
    ),
]
