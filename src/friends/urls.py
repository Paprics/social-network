from django.urls import path

from . import views

app_name = "friends"

urlpatterns = [
    path("friend/send/", views.SendFriendRequestView.as_view(), name="send_friend"),
    path("friend/retract/", views.RetractFriendRequestView.as_view(), name="retract_friend"),
    path("friend/accept/", views.AcceptFriendRequestView.as_view(), name="accept_friend"),
    path("friend/decline/", views.DeclineFriendRequestView.as_view(), name="decline_friend"),
    path("friend/remove/", views.RemoveFriendRequestView.as_view(), name="remove_friend"),
    #
    path("block/", views.BlockUserView.as_view(), name="block_user"),
    path("unblock/", views.UnblockUserView.as_view(), name="unblock_user"),
    #
    path("friends/detail/", views.FriendsDetailView.as_view(), name="friends_detail"),
]
