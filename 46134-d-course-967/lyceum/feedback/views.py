from django.contrib import messages
import django.core.mail
from django.shortcuts import redirect, render, reverse


from feedback.forms import FeedbackFileForm, FeedbackForm, PersonalDataForm
from feedback.models import FeedbackFile
from lyceum.settings import DEFAULT_FROM_EMAIL

__all__ = []


def feedback(request):
    template = "feedback/feedback.html"
    feedback_form = FeedbackForm(request.POST or None)
    personal_data_form = PersonalDataForm(request.POST or None)
    files_form = FeedbackFileForm(request.POST or None)
    if request.method == "POST":
        if feedback_form.is_valid() and personal_data_form.is_valid():
            fb = feedback_form.save(commit=True)
            fb.status = "GET"
            fb.save()
            fb_info = personal_data_form.save(commit=False)
            fb_info.personal_data = fb
            fb_info.save()

            feedback_data = feedback_form.cleaned_data
            personal_data = personal_data_form.cleaned_data

            if "files" in request.FILES:
                for upload_file in request.FILES.getlist("files"):
                    FeedbackFile.objects.create(file=upload_file, feedback=fb)

            head = "Отзыв"
            message = feedback_data["text"]
            sender = DEFAULT_FROM_EMAIL
            recipient = personal_data["mail"]

            django.core.mail.send_mail(
                head,
                message,
                sender,
                [recipient],
                fail_silently=False,
            )

            messages.success(request, "Отзыв отправлен и сохранен!")
            return redirect(reverse("feedback:feedback"))

    context = {
        "feedback_form": feedback_form,
        "personal_data_form": personal_data_form,
        "files_form": files_form,
    }
    return render(request, template, context)


def thanks(request):
    template = "feedback/thanks.html"
    context = {}
    return render(request, template, context)
