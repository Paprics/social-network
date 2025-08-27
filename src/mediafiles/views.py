from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied, ValidationError
from django.http.response import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls.base import reverse_lazy
from django.views.generic.base import View
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.views.generic.list import ListView
from easy_thumbnails.files import get_thumbnailer

from .models import AlbumModel, PhotoModel


class AlbumGalleryView(DetailView):
    model = AlbumModel
    # template_name = "gallery.html"
    template_name = "gall.html"
    context_object_name = "album"
    slug_field = "slug"
    slug_url_kwarg = "album_slug"

    def get_object(self, queryset=None):
        # ищем альбом по пользователю и слагу
        return get_object_or_404(
            AlbumModel.objects.filter(owner__username=self.kwargs["target_user"], is_active=True),
            slug=self.kwargs["album_slug"]
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        album = self.object

        photos = []
        qs = PhotoModel.objects.filter(album=album, is_active=True)

        for photo in qs:
            photos.append({
                "url": photo.image.url,
                "width": photo.image.width,
                "height": photo.image.height,
                "thumb_url": get_thumbnailer(photo.image).get_thumbnail({'size': (300, 300), 'crop': True}).url,
                "description": photo.description or ""
            })

        context["photos"] = photos
        return context



class AlbumListView(ListView):
    template_name = "album_list.html"
    model = AlbumModel
    context_object_name = "albums"

    def get_queryset(self):
        target_username = self.kwargs.get("target_user")
        albums_qs = AlbumModel.objects.filter(owner__username=target_username, is_active=True)

        if target_username == self.request.user.username:
            albums_qs = AlbumModel.objects.filter(owner__username=target_username)
        else:
            albums_qs = [album for album in albums_qs if album.can_view(self.request.user)]

        # Если albums_qs уже список (после фильтрации can_view), то делаем так:
        if isinstance(albums_qs, list):
            albums = albums_qs
        else:
            albums = list(albums_qs)

        # Собираем id последних активных фоток для всех альбомов
        from mediafiles.models import PhotoModel  # подставь свой путь

        for album in albums:
            last_photo = PhotoModel.objects.filter(album=album, is_active=True).order_by("-uploaded_at").first()
            if last_photo and last_photo.image:
                thumb = get_thumbnailer(last_photo.image).get_thumbnail({"size": (200, 200), "crop": True})
                album.cover_url = thumb.url
            else:
                album.cover_url = ""

        return albums


class AlbumCreateView(CreateView):
    model = AlbumModel
    template_name = "album_create.html"
    fields = ["title", "description", "privacy", "is_active", "allow_comments"]

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        # Переадресация на список альбомов текущего пользователя
        return reverse_lazy("mediafiles:album-list", kwargs={"target_user": self.request.user.username})

    def form_invalid(self, form):
        return super().form_invalid(form)


class SettingsAlbumView(UpdateView):
    model = AlbumModel
    template_name = "setting_album.html"
    fields = ["title", "description", "privacy", "is_active", "allow_comments"]

    slug_field = "slug"  # поле модели, по которому искать
    slug_url_kwarg = "album_slug"  # параметр из URL

    context_object_name = "album"

    def get_queryset(self):
        return AlbumModel.objects.filter(owner=self.request.user)

    def get_success_url(self):
        return reverse_lazy("mediafiles:album-list", kwargs={"target_user": self.request.user.username})


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


class AddPhotosToAlbumView(LoginRequiredMixin, View):
    def get(self, request, album_slug):
        album = get_object_or_404(AlbumModel, slug=album_slug, owner=request.user)
        return render(request, "add_photos_to_album.html", {"album": album})

    def post(self, request, *args, **kwargs):
        album_slug = kwargs.get("album_slug")
        album = get_object_or_404(AlbumModel, slug=album_slug, owner=request.user)

        photos = request.FILES.getlist("photos")
        errors = {}

        if not photos:
            errors["photos"] = "Please select at least one photo to upload."

        if errors:
            return render(request, "add_photos_to_album.html", {"album": album, "errors": errors})

        added_photos = []
        for photo_file in photos:
            photo = PhotoModel(image=photo_file, owner=request.user, album=album, is_active=True)
            try:
                photo.full_clean()
                photo.save()
                added_photos.append(photo.id)
            except ValidationError as e:
                errors["photos"] = "; ".join([f"{field}: {', '.join(errs)}" for field, errs in e.message_dict.items()])
                return render(request, "add_photos_to_album.html", {"album": album, "errors": errors})

        return redirect("mediafiles:album-detail", target_user=request.user.username, album_slug=album.slug)


class DeleteAlbumView(LoginRequiredMixin, DeleteView):
    model = AlbumModel
    template_name = "delete_album.html"
    slug_field = "slug"
    slug_url_kwarg = "album_slug"
    context_object_name = "album"

    def get_queryset(self):
        target_user = self.kwargs.get("target_user")
        return AlbumModel.objects.filter(owner__username=target_user)

    def dispatch(self, request, *args, **kwargs):
        obj = self.get_object()
        if obj.owner != request.user:
            raise PermissionDenied("You don't have permission to delete this album.")
        return super().dispatch(request, *args, **kwargs)

    def get_success_url(self):
        return reverse_lazy("mediafiles:album-list", kwargs={"target_user": self.request.user.username})
