from django.http.response import JsonResponse
from django.shortcuts import render
from django.views.generic.base import View
from .models import PhotoModel, AlbumModel


class UploadUserProfilePhotoView(View):
    def post(self, request, *args, **kwargs):
        profile_photo = request.FILES.get('profile_photo')
        if not profile_photo:
            return JsonResponse({"success": False, "error": "No file provided"}, status=400)

        # Название альбома для аватаров — константа
        ALBUM_TITLE = "Profile photos"

        # Пытаемся получить альбом пользователя с таким названием
        album, created = AlbumModel.objects.get_or_create(
            owner=request.user,
            title=ALBUM_TITLE,
            defaults={'privacy': 'private', 'is_active': True}
        )
        # В случае создания save() сработает и слаг тоже будет

        # Создаем фото и привязываем к альбому
        photo_object = PhotoModel(
            image=profile_photo,
            owner=request.user,
            album=album,
            context='avatar',
        )

        try:
            photo_object.full_clean()  # валидация
            photo_object.save()
        except ValidationError as e:
            return JsonResponse({"success": False, "errors": e.message_dict}, status=400)

        return JsonResponse({"success": True, "photo_id": photo_object.id, "album_slug": album.slug})

