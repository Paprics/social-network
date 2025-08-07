from django.urls import path
from django.views.generic import TemplateView

app_name = "favorites"

urlpatterns = [
    path('fav/', TemplateView.as_view(template_name="check.html"), name="favorites_index")
]
