from django.contrib.auth import get_user_model, login
from django.contrib.auth.views import LoginView, LogoutView, PasswordResetView
from django.http.response import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls.base import reverse_lazy, reverse
from django.views.generic.base import RedirectView
from django.views.generic.edit import CreateView, DeleteView
from django.utils.http import urlsafe_base64_decode
from accounts.utils.utils import send_registration_email, TokenGenerator

from .forms import LoginForm, UserRegistrationForm


# REGISTRATION
class SignUpView(CreateView):
    model = get_user_model()
    form_class = UserRegistrationForm
    template_name = "registration/signup.html"
    success_url = reverse_lazy("main:index")

    # def post(self, request, *args, **kwargs):
    #     print(request.POST)
    #     return super().post(request, *args, **kwargs)

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.is_email_verified = False
        self.object.save()

        send_registration_email(self.object, self.request)

        login(self.request, self.object)

        return HttpResponseRedirect(self.get_success_url())

    def form_invalid(self, form):
        print(form.errors)
        return super().form_invalid(form)


class EmailVerificationView(RedirectView):

    def get_redirect_url(self, uidb64, token, *args, **kwargs):
        try:
            pk = int(urlsafe_base64_decode(uidb64).decode())
            current_user = get_user_model().objects.get(pk=pk)
        except (get_user_model().DoesNotExist, ValueError, TypeError):
            return reverse("accounts:activation-failed")

        if current_user.is_email_verified:
            return reverse("accounts:activation-failed")

        if TokenGenerator().check_token(current_user, token):
            current_user.is_email_verified = True
            current_user.save()
            login(self.request, current_user)
            return reverse("accounts:activation-success")

        return reverse("accounts:activation-failed")


class LoginView(LoginView):
    template_name = "registration/login.html"
    form_class = LoginForm
    success_url = reverse_lazy("main:index")

    # def form_valid(self, form):
    #     # 💥 Вот тут ставишь точку останова (например, PyCharm: клик слева от строки)
    #     print("CLEANED DATA:", form.cleaned_data)  # или смотри в отладчике
    #     return super().form_valid(form)


# class LoginView(LoginView):
#     template_name = "registration/login.html"
#     authentication_form = AuthenticationForm
#     redirect_authenticated_user = True
#
#     def get_success_url(self):
#         return reverse_lazy("common:index")


class Logout(LogoutView): ...


class PasswordReset(PasswordResetView): ...


class DeleteView(DeleteView): ...
