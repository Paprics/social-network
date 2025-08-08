from django.urls import path
from django.views.generic import TemplateView

from . import views

app_name = "mediafiles"

urlpatterns = [
    path("files/", TemplateView.as_view(template_name="files.html")),
    path("upload/profile-photo/", views.UploadUserProfilePhotoView.as_view(), name="upload_profile_photo"),
    path("albums/create/", views.AlbumCreateView.as_view(), name="album-create"),  # ПОСТАВЬ ВЫШЕ!
    path("albums/<slug:target_user>/", views.AlbumListView.as_view(), name="album-list"),
    path("albums/<slug:target_user>/<slug:album_slug>/", views.AlbumDetailView.as_view(), name="album-detail"),
]
