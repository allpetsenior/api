import os

from channels.routing import ProtocolTypeRouter
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.security.websocket import AllowedHostsOriginValidator
from ai.websocket_url_patterns import websocket_urlpatterns
from ai.middlewares import TokenAuthMiddleware

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'app.settings')
# Initialize Django ASGI application early to ensure the AppRegistry
# is populated before importing code that may import ORM models.
django_asgi_app = get_asgi_application()

application = ProtocolTypeRouter({
    "http": django_asgi_app,
    # Just HTTP for now. (We can add other protocols later.)
    "websocket": AllowedHostsOriginValidator(
        TokenAuthMiddleware(
            URLRouter(websocket_urlpatterns
                      )
        )
    ),
})
