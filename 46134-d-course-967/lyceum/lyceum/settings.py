import os
from pathlib import Path

from django.utils.translation import gettext_lazy as _
import environ

env = environ.Env(
    DJANGO_DEBUG=(bool, True),
    DJANGO_SECRET_KEY=(str, "SECRET_KEY"),
    DJANGO_ALLOWED_HOSTS=(list, ["localhost", "127.0.0.1"]),
    DJANGO_ALLOW_REVERSE=(str, "false"),
    DJANGO_MAIL=(str, "example@example.com"),
    DJANGO_DEFAULT_USER_IS_ACTIVE=(str, "false"),
    DJANGO_MAX_AUTH_ATTEMPTS=(int, 5),
)

BASE_DIR = Path(__file__).resolve().parent.parent

environ.Env.read_env(os.path.join(BASE_DIR.parent, ".env"))

SECRET_KEY = env("DJANGO_SECRET_KEY")

DEBUG = env("DJANGO_DEBUG")

if env("DJANGO_DEFAULT_USER_IS_ACTIVE").lower() in ["false", "n", "no", "0"]:
    DEFAULT_USER_IS_ACTIVE = False
elif env("DJANGO_DEFAULT_USER_IS_ACTIVE").lower() in ["true", "t", "yes", "1"]:
    DEFAULT_USER_IS_ACTIVE = True
else:
    DEFAULT_USER_IS_ACTIVE = False
    if DEBUG:
        DEFAULT_USER_IS_ACTIVE = True

MAX_AUTH_ATTEMPTS = env("DJANGO_MAX_AUTH_ATTEMPTS")

ALLOWED_HOSTS = env("DJANGO_ALLOWED_HOSTS")

ALLOW_REVERSE = (
    False
    if env("DJANGO_ALLOW_REVERSE").lower() in ["false", "n", "no", "0"]
    else True
)

DEFAULT_FROM_EMAIL = env("DJANGO_MAIL")

INSTALLED_APPS = [
    "catalog.apps.CatalogConfig",
    "about.apps.AboutConfig",
    "homepage.apps.HomepageConfig",
    "download.apps.DownloadConfig",
    "feedback.apps.FeedbackConfig",
    "users.apps.UsersConfig",
    "rating.apps.RatingConfig",
    "statistic.apps.StatisticConfig",
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "sorl.thumbnail",
    "tinymce",
    "django_cleanup.apps.CleanupConfig",
    "translation",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "django.middleware.locale.LocaleMiddleware",
    "lyceum.middleware.Middleware",
    "users.middleware.ProxyUserRequestMiddleware",
]

if DEBUG:
    INSTALLED_APPS.append("debug_toolbar")
    MIDDLEWARE.append("debug_toolbar.middleware.DebugToolbarMiddleware")

INTERNAL_IPS = [
    "127.0.0.1",
    "localhost",
]

ROOT_URLCONF = "lyceum.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                "django.template.context_processors.media",
            ],
        },
    },
]

WSGI_APPLICATION = "lyceum.wsgi.application"

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    },
}
# fmt: off
AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth."
                "password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth."
                "password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth."
                "password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth."
                "password_validation.NumericPasswordValidator",
    },
]
# fmt: on

LANGUAGE_CODE = "ru"

LANGUAGES = (
    ("ru", _("Russian")),
    ("en", _("English")),
)

TIME_ZONE = "UTC"

USE_I18N = True

USE_TZ = True

STATIC_URL = "/static/"

STATICFILES_DIRS = [BASE_DIR / "static_dev"]

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

MEDIA_ROOT = BASE_DIR / "media"
MEDIA_URL = "/media/"

LOCALE_PATHS = (BASE_DIR / "locale/",)

EMAIL_BACKEND = "django.core.mail.backends.filebased.EmailBackend"
EMAIL_FILE_PATH = BASE_DIR / "send_mail"

LOGIN_URL = "/auth/login/"
LOGIN_REDIRECT_URL = "/auth/profile/"
LOGOUT_REDIRECT_URL = "/auth/logout/"

AUTHENTICATION_BACKENDS = [
    "users.backends.EmailAuthBackend",
    "django.contrib.auth.backends.ModelBackend",
]
