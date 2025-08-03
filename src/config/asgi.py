# src/config/asgi.py
import os

import django

from config.settings.base import env

# Настраиваем Django до импорта зависимостей
mode = env("MODE", default="dev")
os.environ.setdefault("DJANGO_SETTINGS_MODULE", f"config.settings.{mode}")
django.setup()

# локальные импорты (flake8 не будет ругаться, потому что мы делаем это явно)
from channels.auth import AuthMiddlewareStack  # noqa: E402
from channels.routing import ProtocolTypeRouter, URLRouter  # noqa: E402
from channels.security.websocket import \
    AllowedHostsOriginValidator  # noqa: E402
from django.core.asgi import get_asgi_application  # noqa: E402

import messaging.routing  # noqa: E402

# Django-приложение (обслуживает HTTP)
django_asgi_app = get_asgi_application()

# Главная точка входа для Daphne/Channels
application = ProtocolTypeRouter(
    {
        "http": django_asgi_app,
        "websocket": AllowedHostsOriginValidator(
            AuthMiddlewareStack(URLRouter(messaging.routing.websocket_urlpatterns))
        ),
    }
)
