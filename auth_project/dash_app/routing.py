from django.urls import path
from channels.routing import URLRouter
from . import consumers



websocket_urlpatterns = [
    # path('ws/data/', consumers.DataConsumer.as_asgi()),
    path("ws/live-data/", consumers.LiveDataConsumer.as_asgi()),
]