from django.contrib.auth import get_user_model, login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.views import LoginView, LogoutView, PasswordResetView
from django.http.response import HttpResponseRedirect
from django.urls.base import reverse_lazy
from django.views.generic.edit import CreateView, DeleteView
from accounts.utils.utils import send_registration_email

from . import forms
from .forms import LoginForm, UserRegistrationForm

# REGISTRATION
class SignUpView(CreateView):
    model = get_user_model()
    form_class = UserRegistrationForm
    template_name = 'registration/signup.html'
    success_url = reverse_lazy('main:index')

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



class LoginView(LoginView):
    template_name = 'registration/login.html'
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

class DeleteView(DeleteView):...