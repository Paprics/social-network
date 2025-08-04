from django.db.models.query_utils import Q

from friends.models import FriendRequestModel


class FriendService:
    def send_friend_request(self, from_user, to_user):
        if from_user == to_user:
            raise ValueError("Нельзя добавить себя в друзья")

        existing = FriendRequestModel.objects.filter(
            (Q(from_user=from_user) & Q(to_user=to_user)) |
            (Q(from_user=to_user) & Q(to_user=from_user))
        ).exists()
        if existing:
            raise ValueError("Заявка уже существует в любом направлении")
        if existing:
            raise ValueError("Заявка уже отправлена")

        FriendRequestModel.objects.create(from_user=from_user, to_user=to_user)

    def accept_request(self, from_user, to_user):...

    # Создаём Friendship
    # Удаляем заявку


    def cancel_request(self, from_user, to_user):...

    # Отменяем заявку



    def reject_request(self, from_user, to_user):...

    # Отклоняем заявку

    def remove_friend(self, user1, user2):...

    # Удаляем Friendship


class BlockService:
    pass


