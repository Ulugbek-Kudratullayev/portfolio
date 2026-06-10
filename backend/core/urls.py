from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.http import JsonResponse
from django.urls import include, path


def index(request):
    return JsonResponse(
        {
            "name": "Portfolio API",
            "endpoints": [
                "/api/projects/",
                "/api/projects/<slug>/",
                "/api/contact/",
                "/api/health/",
            ],
        }
    )


urlpatterns = [
    path("", index),
    path("admin/", admin.site.urls),
    path("api/", include("portfolio_api.urls")),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
