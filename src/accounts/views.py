from django.contrib.auth import get_user_model, login, update_session_auth_hash
from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import (LogoutView, PasswordResetCompleteView,
                                       PasswordResetConfirmView,
                                       PasswordResetView)
from django.db.models.query_utils import Q
from django.http.response import HttpResponseForbidden, HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect, render
from django.urls.base import reverse, reverse_lazy
from django.utils.http import urlsafe_base64_decode
from django.views.generic.base import RedirectView, View
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, DeleteView, FormView
from django.views.generic.list import ListView

from accounts.utils.utils import TokenGenerator, send_registration_email
from friends.models import (BlockedUserModel, FriendRequestModel,
                            FriendShipModel)
from geo.models import City, Country, Region, Subregion

from .forms import UserProfileForm, UserRegistrationForm, UserUpdateForm
from .models import UserProfileModel

User = get_user_model()


class UserProfileEditView(LoginRequiredMixin, View):
    template_name = "user_profile_edit.html"

    def dispatch(self, request, *args, **kwargs):
        username = kwargs.get("username")

        if username != request.user.username:
            return HttpResponseForbidden("Nice try, but no.")

        return super().dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        user = get_object_or_404(User, username=kwargs.get("username"))
        profile, _ = UserProfileModel.objects.get_or_create(user=user)

        form_user = UserUpdateForm(instance=user)
        form_profile = UserProfileForm(instance=profile)

        countries = Country.objects.all()
        regions = (
            Region.objects.filter(country=profile.city.country) if profile and profile.city else Region.objects.none()
        )
        subregions = (
            Subregion.objects.filter(region=profile.city.region)
            if profile and profile.city and profile.city.region
            else Subregion.objects.none()
        )
        cities = City.objects.filter(region=profile.city.region) if profile and profile.city else City.objects.none()

        return render(
            request,
            self.template_name,
            {
                "user": user,
                "profile": profile,
                "form_user": form_user,
                "form_profile": form_profile,
                "countries": countries,
                "regions": regions,
                "subregions": subregions,
                "cities": cities,
            },
        )

    def post(self, request, *args, **kwargs):
        user = get_object_or_404(User, username=kwargs.get("username"))
        profile, _ = UserProfileModel.objects.get_or_create(user=user)

        form_user = UserUpdateForm(request.POST, instance=user)
        form_profile = UserProfileForm(request.POST, request.FILES, instance=profile)

        if form_user.is_valid() and form_profile.is_valid():
            # Форма валидна — сохраняем и редиректим
            form_user.save()
            obj_profile = form_profile.save(commit=False)
            obj_profile.user = user
            obj_profile.save()
            return redirect("accounts:user-profile", username=user.username)
        else:
            # Форма не валидна — выводим ошибки и заново показываем форму с данными
            print(f"form_user errors - {form_user.errors}")
            print(f"form_profile errors - {form_profile.errors}")

            countries = Country.objects.all()
            regions = (
                Region.objects.filter(country=profile.city.country)
                if profile and profile.city
                else Region.objects.none()
            )
            subregions = (
                Subregion.objects.filter(region=profile.city.region)
                if profile and profile.city and profile.city.region
                else Subregion.objects.none()
            )
            cities = (
                City.objects.filter(region=profile.city.region) if profile and profile.city else City.objects.none()
            )

            return render(
                request,
                self.template_name,
                {
                    "user": user,
                    "profile": profile,
                    "form_user": form_user,
                    "form_profile": form_profile,
                    "countries": countries,
                    "regions": regions,
                    "subregions": subregions,
                    "cities": cities,
                },
            )


class UserListView(ListView):
    model = User
    context_object_name = "users"
    template_name = "list-all-user.html"


class UserProfileView(DetailView):
    model = User
    slug_field = "username"
    slug_url_kwarg = "username"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._target_user = None

    def get_object(self, *args, **kwargs):
        if self._target_user is None:
            self._target_user = super().get_object(*args, **kwargs)
        return self._target_user

    def get_queryset(self):
        return User.objects.select_related(
            "userprofilemodel__city__region__country"  # цепочка для джойнов, чтоб за 1 запрос подтянуть всё
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        target_user = self.get_object()
        context["target_user"] = target_user

        current_user = self.request.user

        if not current_user.is_authenticated:
            # Аноним, статусы по умолчанию
            context["is_friends"] = False
            context["request_sent"] = False
            context["request_received"] = False
            context["blocked_by_current_user"] = False
            context["blocked_by_object_user"] = False
            return context

        # --- Статусы  ---
        is_friends = FriendShipModel.objects.filter(
            Q(user1=current_user, user2=target_user) | Q(user1=target_user, user2=current_user)
        ).exists()

        # Отправлена заявка от current_user к object_user?
        request_sent = FriendRequestModel.objects.filter(from_user=current_user, to_user=target_user).first()

        # Получена заявка от object_user?
        request_received = FriendRequestModel.objects.filter(from_user=target_user, to_user=current_user).first()

        print(request_sent, request_received)

        # Заблокирован ли ?
        blocked_by_current_user = BlockedUserModel.objects.filter(blocker=current_user, blocked=target_user).exists()

        blocked_by_object_user = BlockedUserModel.objects.filter(blocker=target_user, blocked=current_user).exists()

        context["is_friends"] = is_friends
        context["request_sent"] = request_sent
        context["request_received"] = request_received

        context["blocked_by_current_user"] = blocked_by_current_user
        context["blocked_by_object_user"] = blocked_by_object_user

        return context

    def get_template_names(self):
        current_user = self.request.user
        target_user = self.get_object()  # TODO Dublicate

        # Если просматривает сам себя
        if current_user.id == target_user.id:
            return ["user_own_profile_detail.html"]

        # Если target_user заблокировал current_user — отдаем шаблон блокировки
        if current_user.is_authenticated:
            is_blocked = BlockedUserModel.objects.filter(blocker=target_user, blocked=current_user).exists()
            if is_blocked:
                return ["user_profile_blocked.html"]

        return ["user_profile_detail.html"]


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
