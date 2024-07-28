"""
ASGI config for eco project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/howto/deployment/asgi/
"""

# import os

# from django.core.asgi import get_asgi_application

# os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'eco.settings')

# application = get_asgi_application()

# asgi.py

# study/asgi.py


# import os
# from django.core.asgi import get_asgi_application
# from channels.routing import ProtocolTypeRouter, URLRouter # type: ignore
# from channels.auth import AuthMiddlewareStack # type: ignore
# from channels.security.websocket import AllowedHostsOriginValidator
# import chatting.routing

# os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'study.settings')

# application = ProtocolTypeRouter({
#     "http": get_asgi_application(),
#     "websocket": AuthMiddlewareStack(
#         URLRouter(
#             chatting.routing.websocket_urlpatterns
#         )
#     ),
# })



import os

from channels.auth import AuthMiddlewareStack # type: ignore
from channels.routing import ProtocolTypeRouter, URLRouter # type: ignore
from channels.security.websocket import AllowedHostsOriginValidator # type: ignore
from django.core.asgi import get_asgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'study.settings')
# Initialize Django ASGI application early to ensure the AppRegistry
# is populated before importing code that may import ORM models.
django_asgi_app = get_asgi_application()

import chatting.routing

application = ProtocolTypeRouter(
    {
        "http": django_asgi_app,
        "websocket": AllowedHostsOriginValidator(
            AuthMiddlewareStack(URLRouter(chatting.routing.websocket_urlpatterns))
        ),
    }
)