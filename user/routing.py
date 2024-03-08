from django.urls import path
from . import consumers

websocket_urlpatterns = [
    # path('ws/ac/status/',
    #      consumers.UserConnectivityStatusConsumer.as_asgi()),
    
    # path('ws/test/', consumers.TestConsumer.as_asgi()),
]
