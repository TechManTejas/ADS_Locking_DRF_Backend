import os
from django.core.asgi import get_asgi_application
from django.urls import path
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
from locking.consumers import LockingConsumer

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ads_locking_drf_backend.settings')

application = ProtocolTypeRouter({
    'http': get_asgi_application(),
    'websocket': AuthMiddlewareStack(
        URLRouter(
            [
                # Define websocket URL pattern
                path('ws/locking/', LockingConsumer.as_asgi()),
            ]
        )
    ),
})
