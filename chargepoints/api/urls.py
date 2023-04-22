from django.urls import path

from chargepoints.api.views.chargepoint import ChargepointList, ChargepointDetail

app_name = "chargepoints-api"

urlpatterns = [
    path('chargepoints/', ChargepointList.as_view(), name='chargepoint-list'),
    path('chargepoints/<int:pk>/', ChargepointDetail.as_view(), name='chargepoint-detail'),
]
