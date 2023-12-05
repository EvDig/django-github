import datetime

from django.conf import settings
from django.contrib.auth import login
import django.contrib.auth.decorators
import django.contrib.auth.models
import django.core.mail
from django.core.signing import BadSignature, SignatureExpired, TimestampSigner
from django.http import Http404
from django.shortcuts import get_object_or_404, redirect, render, reverse
from django.utils.timezone import now, timedelta

from lyceum.settings import DEFAULT_FROM_EMAIL
import users.forms
import users.models

__all__ = []


def sign_up(request):
    template = "users/signup.html"
    form = users.forms.RegisterForm(request.POST or None)

    if request.method == "POST":
        if form.is_valid():
            new_user = form.save(commit=False)
            if settings.DEBUG:
                new_user.is_superuser = True
                new_user.is_staff = True
            if not settings.DEFAULT_USER_IS_ACTIVE:
                new_user.is_active = False
            new_user.save()
            users.models.Profile.objects.create(
                user=new_user,
            )

            if not settings.DEFAULT_USER_IS_ACTIVE:
                user_data = form.cleaned_data
                head = "Активация пользователя"
                username = user_data["username"]
                signer = TimestampSigner()
                signed_username = signer.sign(username)
                link = (
                    f"ЧТОБЫ АКТИВИРОВАТЬ АККАУНТ ПЕРЕЙДИ"
                    f" НА auth/activate/{signed_username}"
                )
                message = link
                sender = DEFAULT_FROM_EMAIL
                recipient = user_data["email"]

                django.core.mail.send_mail(
                    head,
                    message,
                    sender,
                    [recipient],
                    fail_silently=False,
                )

            return redirect(reverse("users:login"))

    context = {
        "form": form,
    }

    return render(request, template, context)


def activate(request, username):
    signer = TimestampSigner()
    try:
        username = signer.unsign(
            username,
            max_age=datetime.timedelta(hours=12),
        )
    except (SignatureExpired, BadSignature):
        raise Http404("Signature expired or bad signature found:")
    template = "users/activate.html"
    user = get_object_or_404(
        django.contrib.auth.models.User,
        username=username,
        is_active=False,
    )
    user.is_active = True
    user.save(update_fields=["is_active"])

    login(request, user, backend="django.contrib.auth.backends.ModelBackend")
    context = {}

    return render(request, template, context)


def activate_again(request, username):
    signer = TimestampSigner()
    try:
        username = signer.unsign(
            username,
            max_age=datetime.timedelta(days=7),
        )
    except (SignatureExpired, BadSignature):
        raise Http404("Signature expired or bad signature found:")
    template = "users/activate.html"
    user = get_object_or_404(
        django.contrib.auth.models.User,
        username=username,
        is_active=False,
    )
    date_activate = now() - timedelta(
        weeks=1,
    )
    second_date = user.profile.block_date
    if (
        date_activate.timestamp() <= second_date.timestamp()
    ) and not user.is_active:
        user.is_active = True
        user.profile.attempts_count = 0
        user.save(update_fields=["is_active"])
        user.profile.save()

        login(
            request,
            user,
            backend="django.contrib.auth.backends.ModelBackend",
        )
    context = {}

    return render(request, template, context)


def user_list(request):
    template = "users/user_list.html"

    users_list = django.contrib.auth.models.User.objects.filter(
        is_active=True,
    ).only("username")

    context = {"users": users_list}

    return render(request, template, context)


def user_detail(request, pk):
    template = "users/user_detail.html"

    user_by_id = (
        django.contrib.auth.models.User.objects.filter(pk=pk, is_active=True)
        .select_related("profile")
        .only("email", "first_name", "last_name")
    ).get()

    context = {
        "user": user_by_id,
    }

    return render(request, template, context)


@django.contrib.auth.decorators.login_required()
def user_profile(request):
    template = "users/profile.html"

    user = get_object_or_404(
        django.contrib.auth.models.User,
        id=request.user.id,
    )

    user_form = users.forms.UserChangeForm(request.POST or None, instance=user)

    profile_form = users.forms.ProfileChangeForm(
        request.POST or None,
        request.FILES or None,
        instance=user.profile,
    )

    if request.method == "POST":
        if profile_form.is_valid() and user_form.is_valid():
            user_form.save()
            profile_form.save()

            return redirect(reverse("users:user_profile"))

    context = {
        "user_form": user_form,
        "profile_form": profile_form,
    }

    return render(request, template, context)
