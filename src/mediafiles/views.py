from django.core.exceptions import ValidationError
from django.http.response import JsonResponse
from django.shortcuts import redirect
from django.views.generic.base import View
from django.views.generic.list import ListView

from .models import AlbumModel, PhotoModel


class AlbumDetailView(ListView):
    template_name = "album_detail.html"
    context_object_name = "photos"
    model = PhotoModel
    paginate_by = 20

    def get_queryset(self):
        target_user = self.kwargs.get("target_user")
        album_slug = self.kwargs.get("album_slug")
        return PhotoModel.objects.filter(
            album__owner__username=target_user, album__slug=album_slug, is_active=True
        ).order_by("-uploaded_at")


class AlbumListView(ListView):
    template_name = "album_list.html"
    model = AlbumModel
    context_object_name = "albums"
    # paginate_by = 10

    def get_queryset(self):
        target_username = self.kwargs.get("target_user")
        if target_username == self.request.user.username:
            return AlbumModel.objects.filter(owner__username=target_username)
        else:
            # логику фильтрации для чужого пользователя
            return AlbumModel.objects.filter(owner__username=target_username, is_active=True)


class UploadUserProfilePhotoView(View):
    def post(self, request, *args, **kwargs):
        profile_photo = request.FILES.get("profile_photo")
        if not profile_photo:
            return JsonResponse({"success": False, "error": "No file provided"}, status=400)

        # Название альбома для аватаров — константа
        ALBUM_TITLE = "Profile photos"

        # Пытаемся получить альбом пользователя с таким названием
        album, created = AlbumModel.objects.get_or_create(
            owner=request.user, title=ALBUM_TITLE, defaults={"privacy": "private", "is_active": True}
        )
        # В случае создания save() сработает и слаг тоже будет

        # Создаем фото и привязываем к альбому
        photo_object = PhotoModel(
            image=profile_photo,
            owner=request.user,
            album=album,
            context="avatar",
        )

        try:
            photo_object.full_clean()  # валидация
            photo_object.save()
        except ValidationError as e:
            return JsonResponse({"success": False, "errors": e.message_dict}, status=400)

        return redirect(request.META.get("HTTP_REFERER", "/"))
