from django.contrib.auth import get_user_model, login
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.contrib.auth.views import (LoginView, LogoutView,
                                       PasswordResetConfirmView,
                                       PasswordResetView, PasswordResetCompleteView)
from django.http.response import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls.base import reverse, reverse_lazy
from django.utils.http import urlsafe_base64_decode
from django.views.generic.base import RedirectView, View
from django.views.generic.edit import CreateView, DeleteView

from accounts.utils.utils import TokenGenerator, send_registration_email

from .forms import LoginForm, UserRegistrationForm


# RESET PASSWORD
class ResetPasswordView(PasswordResetView):
    template_name = "registration/reset_password.html"
    email_template_name = "reset_password_email.html"
    success_url = reverse_lazy("accounts:password_reset_done")

    # def get_success_url(self):
    #     return reverse_lazy('accounts:password_reset_done')


class CustomPasswordResetConfirmView(PasswordResetConfirmView):
    template_name = "registration/reset_password_confirm.html"
    success_url = reverse_lazy("accounts:password_reset_complete")
    # TODO: Prevent password reset token reuse after user login (invalidate old tokens)


class CustomPasswordResetCompleteView(PasswordResetCompleteView):
    template_name = 'registration/reset_password_complete.html'


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


class CustomLoginView(View):
    def get(self, request):
        if request.user.is_authenticated:
            return redirect("main:index")
        form = AuthenticationForm()
        return render(request, "registration/login.html", {"form": form})

    def post(self, request):
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            # Тут логиним пользователя
            login(request, form.get_user())
            return redirect("main:index")
        return render(request, "registration/login.html", {"form": form})


class Logout(LogoutView): ...


class DeleteView(DeleteView): ...
