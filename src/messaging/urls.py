from django.urls.conf import path

from messaging import views

app_name = "messaging"

urlpatterns = [
    path("chat/", views.ChatView.as_view(), name="chat"),
]
