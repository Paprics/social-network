from django.urls import path

from . import views

app_name = "friends"

urlpatterns = [
    path("friend/send/", views.SendFriendRequestView.as_view(), name="send_friend"),
    path("friend/retract/", views.RetractFriendRequestView.as_view(), name="retract_friend"),
    path("friend/accept/", views.AcceptFriendRequestView.as_view(), name="accept_friend"),
    path("friend/decline/", views.DeclineFriendRequestView.as_view(), name="decline_friend"),
    #
    path("friends/detail/", views.FriendsDetailView.as_view(), name="friends_detail"),
]
