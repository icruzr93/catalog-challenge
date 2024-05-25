from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/catalog/", include("app.catalog.urls")),
    path("api/core/", include("app.core.urls")),
]
