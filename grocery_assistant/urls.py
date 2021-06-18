from django.conf import settings
from django.conf.urls import handler404, handler500
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from django.views.generic import TemplateView

from . import views

handler404 = "grocery_assistant.views.page_not_found"  # noqa
handler500 = "grocery_assistant.views.server_error"  # noqa


urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("recipe.urls")),
    path("auth/", include("users.urls")),
    path("auth/", include("django.contrib.auth.urls")),
    path("about/", include("about.urls", namespace="about")),
    path("api/", include("api.urls")),
    path("redoc/", TemplateView.as_view(template_name="redoc.html"),
         name="redoc"),
    path("404/", views.page_not_found),
    path("500/", views.server_error),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL,
                          document_root=settings.STATIC_ROOT)
