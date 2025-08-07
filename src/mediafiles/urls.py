from django.urls import path
from django.views.generic import TemplateView

app_name = 'mediafiles'

urlpatterns = [
    path("files/", TemplateView.as_view(template_name='files.html')),
]
