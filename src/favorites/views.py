from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.contenttypes.models import ContentType
from django.http import JsonResponse, HttpResponseBadRequest
from django.shortcuts import get_object_or_404, redirect
from django.views import View
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
            user=current_user,
            content_type=content_type,
            object_id=target_user.id
        ).exists()

        if exists:
            return JsonResponse({"error": "Already in favorites"}, status=400)

        FavoriteModel.objects.create(
            user=current_user,
            content_type=content_type,
            object_id=target_user.id
        )
        return redirect(request.META.get('HTTP_REFERER', '/'))




class RemoveFavoriteUserView(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        target_user_id = request.POST.get("user_id")
        if not target_user_id or not target_user_id.isdigit():
            return HttpResponseBadRequest("Invalid user_id")

        target_user = get_object_or_404(User, id=int(target_user_id))
        current_user = request.user

        content_type = ContentType.objects.get_for_model(target_user)

        favorite = FavoriteModel.objects.filter(
            user=current_user,
            content_type=content_type,
            object_id=target_user.id
        ).first()

        if not favorite:
            return JsonResponse({"error": "Not found in favorites"}, status=404)

        favorite.delete()
        return JsonResponse({"success": "Removed from favorites"})


