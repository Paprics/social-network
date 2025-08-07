from django.urls import path
from django.views.generic import TemplateView
from favorites import views

app_name = "favorites"

urlpatterns = [
    path('favorites/', TemplateView.as_view(template_name="list_favorite.html"), name="list_favorites"),
    path('favorite/user/add/', views.AddFavoriteUserView.as_view(), name="add_favorite_user"),
    path('favorites/user/remove/', views.RemoveFavoriteUserView.as_view(), name="remove_favorite_user"),
]
