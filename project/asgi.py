"""
ASGI config for project project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/6.0/howto/deployment/asgi/
"""

import os
import sys,asyncio

from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter,URLRouter
from channels.auth import AuthMiddlewareStack

if sys.platform == "win32":
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'project.settings.dev')

django_asgi_app = get_asgi_application()

from traverse import routing

application=ProtocolTypeRouter({
    "http":django_asgi_app,
    "websocket":AuthMiddlewareStack(
        URLRouter(routing.websocket_urlpatterns)
        ),
})