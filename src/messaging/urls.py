from django.urls import path

from . import views

app_name = "messaging"

urlpatterns = [
    path("chat/<str:room_name>/", views.ChatView.as_view(), name="chat"),
    # ЗАГЛУШКИ
    path("chat/<str:group_name>/edit/", views.edit_chatroom, name="edit-chatroom"),
    path("chat/<str:group_name>/upload/", views.chat_file_upload, name="chat-file-upload"),
    path("chat/<str:group_name>/leave/", views.chatroom_leave, name="chatroom-leave"),
]
