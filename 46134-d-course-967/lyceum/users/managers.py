from django.contrib.auth.base_user import BaseUserManager

__all__ = []


class UserManager(BaseUserManager):
    def active(self):
        return (
            self.get_queryset()
            .filter(
                is_active=True,
            )
            .select_related("profile")
            .only("username")
        )

    def by_mail(self, email):
        return (
            self.get_queryset()
            .filter(
                email=email,
                is_active=True,
            )
            .select_related("profile")
            .only("email", "first_name", "last_name")
        )

    # fmt: off
    def normalize_email(self, email_in):
        if "@" not in email_in:
            return None
        email = super().normalize_email(email_in)
        if "+" in email:
            name, domain = email.split("+")
            email = name + domain[domain.index("@"):]
        email = email.lower()
        email = email.replace("@ya.ru", "@yandex.ru", 1)
        name = email[:email.index("@")]
        domain = email[email.index("@"):]
        if "@gmail.com" in email:
            name = name.replace(".", "")
        elif "@yandex.ru" in email:
            name = name.replace(".", "-")
        return name + domain
    # fmt: on
