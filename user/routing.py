from django.urls import path
from . import consumers

websocket_urlpatterns = [
    path('ws/ac/status/<str:user_id>/',
         consumers.UserConnectivityStatusConsumer.as_asgi()),
]
