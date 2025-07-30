from django.contrib.auth import get_user_model, login, update_session_auth_hash
from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import (LogoutView, PasswordResetCompleteView,
                                       PasswordResetConfirmView,
                                       PasswordResetView)
from django.http.response import HttpResponseRedirect
from django.shortcuts import redirect, render
from django.urls.base import reverse, reverse_lazy
from django.utils.http import urlsafe_base64_decode
from django.views.generic.base import RedirectView, View
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, DeleteView, FormView

from accounts.utils.utils import TokenGenerator, send_registration_email

from .forms import UserRegistrationForm

User = get_user_model()

class UserProfileView(DetailView):
    model = User
    slug_field = "username"          # говорим Django, что slug = username
    slug_url_kwarg = "username"      # это имя из URLconf
    template_name = 'user_profile_detail.html'


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
    template_name = "registration/reset_password_complete.html"


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


class Logout(LogoutView):
    next_page = reverse_lazy("main:index")


class DeleteAccountView(LoginRequiredMixin, DeleteView):
    model = get_user_model()
    success_url = reverse_lazy("accounts:delete_account_success")  # ссылка на success страницу
    template_name = "delete_account.html"

    def get_object(self, queryset=None):
        return self.request.user


class ChangePasswordView(LoginRequiredMixin, FormView):
    template_name = "change_password.html"
    form_class = PasswordChangeForm
    success_url = reverse_lazy("accounts:change_password_success")

    def get_form(self, form_class=None):
        return self.form_class(user=self.request.user, **self.get_form_kwargs())

    def form_valid(self, form):
        user = form.save()
        update_session_auth_hash(self.request, user)  # Чтобы сессия не слетела после смены пароля
        return super().form_valid(form)
