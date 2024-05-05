import os
from django.core.asgi import get_asgi_application
from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
import game.routing  # Import your app's routing

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'artic_game.settings')

application = ProtocolTypeRouter({
    "http": get_asgi_application(),  # Defines the Django views for HTTP URLs
    "websocket": AuthMiddlewareStack(
        URLRouter(
            game.routing.websocket_urlpatterns  # Use your app's WebSocket URL patterns
        )
    ),
})
