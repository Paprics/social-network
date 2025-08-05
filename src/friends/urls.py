from django.urls import path
from django.views.generic.base import TemplateView
from . import views

app_name = 'friends'

urlpatterns = [
    path('friend/send/', views.SendFriendRequestView.as_view(), name='send_friend'),
    path('friend/retract/', views.RetractFriendRequestView.as_view(), name='retract_friend'),
    path('friend/accept/', views.AcceptFriendRequestView.as_view(), name='accept_friend'),
]

# POST    /friends/request/          # отправить заявку (from_user — берём из auth, to_user в теле)
# DELETE  /friends/request/          # отменить заявку (from_user из auth, to_user в теле)
# POST    /friends/request/accept/   # принять заявку (to_user из auth, from_user в теле)
# POST    /friends/request/reject/   # отклонить заявку (to_user из auth, from_user в теле)
# DELETE  /friends/delete/            # удалить друга (user из auth, friend_id в теле)

# POST    /friends/block/             # заблокировать пользователя (user из auth, blocked_id в теле)
# POST    /friends/unblock/           # разблокировать пользователя (user из auth, blocked_id в теле)

