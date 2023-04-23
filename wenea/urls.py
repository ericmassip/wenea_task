from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("chargepoints.urls")),

    # Login and logout views for the DRF browsable API
    path("api-auth/", include("rest_framework.urls")),
]
