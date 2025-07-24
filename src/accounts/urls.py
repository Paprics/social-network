from django.contrib.auth.views import PasswordResetCompleteView
from django.urls.conf import path
from django.views.generic.base import TemplateView

from . import views

app_name = "accounts"

urlpatterns = [
    #
    path("login/", views.LoginView.as_view(), name="login"),
    path("logout/", views.LogoutView.as_view(), name="logout"),
    # REGISTRATION
    path("signup/", views.SignUpView.as_view(), name="signup"),
    path("activate/<uidb64>/<token>/", views.EmailVerificationView.as_view(), name="verify_email"),
    path(
        "activation-success/",
        TemplateView.as_view(template_name="registration/activation_success.html"),
        name="activation-success",
    ),
    path(
        "activation-failed/",
        TemplateView.as_view(template_name="registration/activation_failed.html"),
        name="activation-failed",
    ),
    # RESET PASSWORD
    # STEP 1
    path("password-reset/", views.ResetPasswordView.as_view(), name="password_reset"),
    path(
        "password-reset/done/",
        TemplateView.as_view(template_name="registration/reset_password_done.html"),
        name="password_reset_done",
    ),
    # STEP 2
    path("reset/<uidb64>/<token>/", views.CustomPasswordResetConfirmView.as_view(), name="password_reset_confirm"),
    path("reset-complete/done/", views.CustomPasswordResetCompleteView.as_view(), name="password_reset_complete"),

    # OTHER
    path("delete/", views.DeleteView.as_view(), name="delete"),
]
