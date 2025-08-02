# dev.py
import os

from config.settings.base import *  # noqa: F403

# SECRET_KEY = os.environ.get("DJANGO_SECRET_KEY")

DEBUG = True

ALLOWED_HOSTS = ["localhost", "127.0.0.1"]

INSTALLED_APPS += [  # noqa: F405
    "django_extensions",
    "debug_toolbar",
]

MIDDLEWARE += ["debug_toolbar.middleware.DebugToolbarMiddleware"]  # noqa: F405

# STATIC SETTINGS
STATIC_URL = "/static/"
STATICFILES_DIRS = [  # Include custom static directory (e.g. Source/static) for development
    BASE_DIR / "static"  # noqa: F405
]

# Debug Toolbar
INTERNAL_IPS = [
    "127.0.0.1",
]

# GITHUB CI
if os.environ.get("GITHUB_WORKFLOW"):
    DATABASES = {
        "default": {  # GitHub Action
            "ENGINE": "django.db.backends.postgresql",
            "NAME": "postgres",
            "USER": "postgres",
            "PASSWORD": "postgres",
            "HOST": "0.0.0.0",
            "PORT": 5432,
        }
    }
else:
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.sqlite3",
            "NAME": BASE_DIR / "db.sqlite3",  # noqa: F405
        },
    }

# message broker для Django Channels
# CHANNEL_LAYERS = {
#     "default": {
#         "BACKEND": "channels.layers.InMemoryChannelLayer",
#     }
# }

CHANNEL_LAYERS = {
    "default": {
        "BACKEND": "channels_redis.core.RedisChannelLayer",
        "CONFIG": {
            "hosts": [(os.getenv("REDIS_HOST", "localhost"), int(os.getenv("REDIS_PORT", 6379)))],
        },
    },
}
