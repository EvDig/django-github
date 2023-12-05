from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

from lyceum import settings
import statistic.urls
import users.urls


urlpatterns = [
    path("", include("homepage.urls")),
    path("catalog/", include("catalog.urls")),
    path("about/", include("about.urls")),
    path("admin/", admin.site.urls),
    path("download/", include("download.urls")),
    path("feedback/", include("feedback.urls")),
    path("auth/", include(users.urls)),
    path("auth/", include("django.contrib.auth.urls")),
    path("statistic/", include(statistic.urls)),
]


if settings.DEBUG:
    import debug_toolbar

    urlpatterns.append(path("__debug__/", include(debug_toolbar.urls)))
    urlpatterns += static(
        settings.MEDIA_URL,
        document_root=settings.MEDIA_ROOT,
    )
