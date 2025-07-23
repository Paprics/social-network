from string import Template

from django.urls.conf import path
from django.views.generic.base import TemplateView

from . import views

app_name = "accounts"

urlpatterns = [
    path("login/", views.LoginView.as_view(), name="login"),
    path("logout/", views.LogoutView.as_view(), name="logout"),
    path("signup/", views.SignUpView.as_view(), name="signup"),
    path("activate/<uidb64>/<token>/", views.EmailVerificationView.as_view(), name="verify_email"),
    path('activation-success/', TemplateView.as_view(template_name='registration/activation_success.html'), name='activation-success'),
    path('activation-failed/', TemplateView.as_view(template_name='registration/activation_failed.html'), name='activation-failed'),
    path("delete/", views.DeleteView.as_view(), name="delete"),
]
