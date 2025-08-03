from django.urls import path
from django.views.generic.base import TemplateView

app_name = 'friends'

urlpatterns = [
    path('friends/', TemplateView.as_view(template_name='check_status.html')),
]
