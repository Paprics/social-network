from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.db.models.query_utils import Q

from friends.models import FriendRequestModel, FriendShipModel

User = get_user_model()


class FriendService:
    def accept_friend_request(self, from_user, to_user):
        try:
            friend_request = FriendRequestModel.objects.get(from_user=from_user, to_user=to_user)

            friendship = FriendShipModel(user1=from_user, user2=to_user)
            friendship.save()

            friend_request.delete()

        except FriendRequestModel.DoesNotExist:
            raise ValidationError("Friend request not found")



    def send_friend_request(self, from_user, to_user):
        if from_user == to_user:
            raise ValueError("Нельзя добавить себя в друзья")

        existing = FriendRequestModel.objects.filter(
            (Q(from_user=from_user) & Q(to_user=to_user)) |
            (Q(from_user=to_user) & Q(to_user=from_user))
        ).exists()
        if existing:
            raise ValueError("Заявка уже существует в любом направлении")

        FriendRequestModel.objects.create(from_user=from_user, to_user=to_user)

    def retract_friend_request(self, from_user, to_user):
        try:
            request = FriendRequestModel.objects.get(from_user=from_user, to_user=to_user)
            request.delete()

        except FriendRequestModel.DoesNotExist:
            raise ValueError("Заявка на дружбу не найдена или уже отменена")






    def reject_request(self, from_user, to_user):...

    # Отклоняем заявку

    def remove_friend(self, user1, user2):...

    # Удаляем Friendship


class BlockService:
    pass


