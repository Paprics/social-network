from django.urls import path

from favorites import views

app_name = "favorites"

urlpatterns = [
    path("favorites/", views.FavoriteListView.as_view(), name="list_favorites"),
    path("favorite/user/add/", views.AddFavoriteUserView.as_view(), name="add_favorite_user"),
    path("favorites/user/remove/", views.RemoveFavoriteUserView.as_view(), name="remove_favorite_user"),
]
