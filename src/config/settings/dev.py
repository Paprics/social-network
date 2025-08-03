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
if os.environ.get("MODE_CHANNEL_LAYERS") == '0':
    CHANNEL_LAYERS = {
        "default": {
            "BACKEND": "channels.layers.InMemoryChannelLayer",
        }
    }
elif os.environ.get("MODE_CHANNEL_LAYERS") == '1':
    CHANNEL_LAYERS = {
        "default": {
            "BACKEND": "channels_redis.core.RedisChannelLayer",
            "CONFIG": {
                "hosts": [(os.getenv("REDIS_HOST", "localhost"), int(os.getenv("REDIS_PORT", 6379)))],
            },
        },
    }
else:
    raise RuntimeError("MODE_CHANNEL_LAYERS must be 0 (InMemory) or 1 (Redis)")

# DATABASES
if os.environ.get("GITHUB_WORKFLOW"):
    # GitHub Actions → PostgreSQL (CI)
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.postgresql",
            "NAME": "postgres",
            "USER": "postgres",
            "PASSWORD": "postgres",
            "HOST": "0.0.0.0",
            "PORT": 5432,
        }
    }

elif os.environ.get("DOCKER_ENV") == "1":
    # Docker → PostgreSQL (берёт переменные из .env)
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.postgresql",
            "NAME": os.environ.get("POSTGRES_DB"),
            "USER": os.environ.get("POSTGRES_USER"),
            "PASSWORD": os.environ.get("POSTGRES_PASSWORD"),
            "HOST": os.environ.get("POSTGRES_HOST", "postgres_db"),
            "PORT": os.environ.get("POSTGRES_PORT", 5432),
        }
    }
elif os.environ.get("MODE_DATABASE") == "0":
    # По умолчанию SQLite (чисто для разработки без всего)
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.sqlite3",
            "NAME": BASE_DIR / "db.sqlite3",
        }
    }
elif os.environ.get("MODE_DATABASE") == "1":
    # Локальная PostgreSQL
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.postgresql",
            "NAME": os.environ.get("POSTGRES_DB"),
            "USER": os.environ.get("POSTGRES_USER"),
            "PASSWORD": os.environ.get("POSTGRES_PASSWORD"),
            "HOST": os.environ.get("POSTGRES_HOST"),
            "PORT": os.environ.get("POSTGRES_PORT"),
        }
    }
else:
    raise RuntimeError("MODE_DATABASE is not set correctly (expected 0 or 1)")
