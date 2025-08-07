from collections import defaultdict

from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.contenttypes.models import ContentType
from django.http import HttpResponseBadRequest, JsonResponse
from django.shortcuts import get_object_or_404, redirect
from django.views import View
from django.views.generic.base import TemplateView

from favorites.models import FavoriteModel

User = get_user_model()


class AddFavoriteUserView(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        target_user_id = request.POST.get("user_id")
        if not target_user_id or not target_user_id.isdigit():
            return HttpResponseBadRequest("Invalid user_id")

        target_user = get_object_or_404(User, id=int(target_user_id))
        current_user = request.user

        content_type = ContentType.objects.get_for_model(User)  # модель, а не экземпляр

        exists = FavoriteModel.objects.filter(
            user=current_user, content_type=content_type, object_id=target_user.id
        ).exists()

        if exists:
            return JsonResponse({"error": "Already in favorites"}, status=400)

        FavoriteModel.objects.create(user=current_user, content_type=content_type, object_id=target_user.id)
        return redirect(request.META.get("HTTP_REFERER", "/"))


class RemoveFavoriteUserView(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        target_user_id = request.POST.get("user_id")
        if not target_user_id or not target_user_id.isdigit():
            return HttpResponseBadRequest("Invalid user_id")

        target_user = get_object_or_404(User, id=int(target_user_id))
        current_user = request.user

        content_type = ContentType.objects.get_for_model(target_user)

        favorite = FavoriteModel.objects.filter(
            user=current_user, content_type=content_type, object_id=target_user.id
        ).first()

        if not favorite:
            return JsonResponse({"error": "Not found in favorites"}, status=404)

        favorite.delete()
        return redirect(request.META.get("HTTP_REFERER", "/"))


class FavoriteListView(TemplateView):
    template_name = "list_favorite.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user

        grouped = defaultdict(list)

        favorites = user.favorites.all().select_related("content_type")

        for fav in favorites:
            model = fav.content_type.model_class()
            obj = fav.content_object
            grouped[model].append(obj)

        # Трансформируем в список словарей с нужными названиями
        context["grouped_favorites"] = [
            {"model_name": model.__name__, "verbose_name": model._meta.verbose_name_plural.title(), "objects": objs}
            for model, objs in grouped.items()
        ]

        return context
