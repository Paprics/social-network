from django.contrib.auth.views import LoginView, LogoutView, PasswordResetView
from django.urls.base import reverse_lazy


class Login(LoginView):
    fields = ("email", "password", "phone_number")


class Logout(LogoutView):...


class PasswordReset(PasswordResetView):...


