from django.contrib import admin
from django.urls import path

from app.catalog.urls import products_urlpatterns
from app.core.urls import users_urlpatterns


urlpatterns = [
    path("admin/", admin.site.urls),
]


# add new urls
urlpatterns += products_urlpatterns
urlpatterns += users_urlpatterns
