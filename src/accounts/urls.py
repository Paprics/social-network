from django.urls.conf import path
from django.views.generic.base import TemplateView

from . import views

app_name = "accounts"

urlpatterns = [
    #
    path("login/", views.CustomLoginView.as_view(), name="login"),
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
    path(
        "reset/invalid/",
        TemplateView.as_view(template_name="registration/password_reset_invalid.html"),
        name="password_reset_invalid",
    ),
    # OTHER
    path("delete-account/", views.DeleteAccountView.as_view(), name="delete"),
    path(
        "delete-account/success/",
        TemplateView.as_view(template_name="delete_account_success.html"),
        name="delete_account_success",
    ),
    path("chenge-password/", views.ChangePasswordView.as_view(), name="chenge_password"),
    path(
        "change-password/success/",
        TemplateView.as_view(template_name="change_password_complete.html"),
        name="change_password_success",
    ),
    # User profile
    path("profile/<str:username>/", views.UserProfileView.as_view(), name="user-profile"),
    path("profile/<str:username>/edit/", views.UserProfileEditView.as_view(), name="user-profile-edit"),
    path("users/", views.UserListView.as_view(), name="user-list"),
]
