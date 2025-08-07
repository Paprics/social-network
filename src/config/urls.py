# urls.py
from django.conf import settings
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("main.urls", namespace="main")),
    path("", include("accounts.urls", namespace="accounts")),
    path("", include("messaging.urls", namespace="messaging")),
    path("", include("geo.urls", namespace="geo")),
    path("", include("friends.urls", namespace="friends")),
    path("", include("favorites.urls", namespace="favorites")),
    path("media/", include("mediafiles.urls", namespace="media")),
]

# DEBUG TOOLBAR
if settings.DEBUG:
    import debug_toolbar

    urlpatterns += [path("__debug__/", include(debug_toolbar.urls))]
