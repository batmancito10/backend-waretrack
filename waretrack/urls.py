from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include('apps.base.api.urls')),
    path("", include('apps.user.api.urls')),
    path("", include('apps.company.api.urls')),
    path("", include('apps.catalog.api.urls')),
    path("", include('apps.supply.api.urls')),
]
