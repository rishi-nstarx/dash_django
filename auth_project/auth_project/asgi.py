import os
from django.core.asgi import get_asgi_application
from channels.routing import URLRouter, ProtocolTypeRouter
from channels.auth import AuthMiddlewareStack

import dash_app.routing

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'auth_project.settings')

application = ProtocolTypeRouter({
    'http': get_asgi_application(),
    'websocket': AuthMiddlewareStack(
        URLRouter(
            dash_app.routing.websocket_urlpatterns
            
        )
    )
})