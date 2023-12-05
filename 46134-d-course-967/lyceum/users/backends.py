import django.conf
from django.contrib.auth.backends import ModelBackend
import django.core.mail
from django.core.signing import TimestampSigner
import django.utils.timezone

import users.models

__all__ = []


class EmailAuthBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            if "@" not in username:
                get_user = users.models.User.objects.get(username=username)
            else:
                mail = users.models.User.objects.normalize_email(username)
                get_user = users.models.User.objects.by_mail(mail).get()
        except users.models.User.DoesNotExist:
            return None
        else:
            if get_user.check_password(password) and get_user.is_active:
                if not hasattr(get_user, "profile"):
                    users.models.Profile.objects.create(
                        user=get_user,
                    )
                get_user.profile.attempts_count = 0
                get_user.profile.save()
                return get_user
            get_user.profile.attempts_count += 1
            get_user.profile.save()
            if (
                get_user.profile.attempts_count
                >= django.conf.settings.MAX_AUTH_ATTEMPTS
            ):
                get_user.is_active = False
                get_user.save()
                get_user.profile.block_date = django.utils.timezone.now()
                get_user.profile.save()

                signer = TimestampSigner()
                head = "Восстановление аккаунта"
                signed_username = signer.sign(get_user.username)
                base = "ЧТОБЫ ВОССТАНОВИТЬ ПЕРЕЙДИ НА "
                message = base + f"auth/activate_again/{signed_username}"
                sender = django.conf.settings.DEFAULT_FROM_EMAIL
                recipient = get_user.email

                django.core.mail.send_mail(
                    head,
                    message,
                    sender,
                    [recipient],
                    fail_silently=False,
                )
        return None
