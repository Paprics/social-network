from django.contrib.auth import get_user_model
from django.contrib.auth.views import LoginView, LogoutView, PasswordResetView
from django.http.response import HttpResponseRedirect
from django.urls.base import reverse_lazy
from django.views.generic.edit import CreateView, DeleteView

from . import forms


class SignUpView(CreateView):
    model = get_user_model()
    form_class = forms.SignupForm
    template_name = "registration/signup.html"
    success_url = reverse_lazy("login")

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.is_active = False
        self.object.save()

        # send_registration_emeil()

        return HttpResponseRedirect(self.get_success_url())


class DeleteView(DeleteView):
    pass


class Login(LoginView):
    fields = ("email", "password", "phone_number")


class Logout(LogoutView): ...


class PasswordReset(PasswordResetView): ...
