from django.urls import path
from django.views.generic import TemplateView
from . import views

app_name = 'mediafiles'

urlpatterns = [
    path("files/", TemplateView.as_view(template_name='files.html')),
    path('upload/profile-photo/', views.UploadUserProfilePhotoView.as_view(), name='upload_profile_photo'),

]
