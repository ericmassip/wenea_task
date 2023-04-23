from django.urls import path, include

from chargepoints.views import LobbyView

urlpatterns = [
    # API v1
    path('api/01/', include('chargepoints.api.urls', namespace="01")),

    # Lobby view where users are notified of every charge point status change
    path('lobby', LobbyView.as_view(), name='lobby'),
]
