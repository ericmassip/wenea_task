from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),

    # API v1
    path('api/01/', include('chargepoints.api.urls', namespace="01")),

    # Login and logout views for the DRF browsable API
    path("api-auth/", include("rest_framework.urls")),
]
