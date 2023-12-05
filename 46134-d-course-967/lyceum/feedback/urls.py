from django.urls import path

import feedback.views

app_name = "feedback"

urlpatterns = [
    path("", feedback.views.feedback, name="feedback"),
    path("thanks/", feedback.views.thanks, name="thanks"),
]
