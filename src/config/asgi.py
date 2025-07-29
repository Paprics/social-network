# src/config/asgi.py
import os

import django
from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.security.websocket import AllowedHostsOriginValidator
from django.core.asgi import get_asgi_application

import messaging.routing
from config.settings.base import env  # импортируем env для работы с .env

# Подтягиваем MODE из .env (если не задано – используем 'dev')
mode = env("MODE", default="dev")
os.environ.setdefault("DJANGO_SETTINGS_MODULE", f"config.settings.{mode}")

# Явно инициализируем Django (чтобы избежать сюрпризов при импортах)
django.setup()

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
