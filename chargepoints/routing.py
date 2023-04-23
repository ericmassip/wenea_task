from django.urls import re_path

from chargepoints.consumers import ChargepointsConsumer

websocket_urlpatterns = [
    re_path(r"ws/chargepoints-lobby/", ChargepointsConsumer.as_asgi()),
]
