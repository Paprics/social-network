from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.db.models.query_utils import Q

from friends.models import FriendRequestModel, FriendShipModel

User = get_user_model()


class FriendService:
    def remove_friend(self, user_a, user_b):
        """Удаляет дружбу между двумя пользователями, не зависит от порядка."""
        friendship = FriendShipModel.objects.filter(
            Q(user1=user_a, user2=user_b) | Q(user1=user_b, user2=user_a)
        ).first()

        if not friendship:
            raise ValidationError("Friendship does not exist")

        friendship.delete()

    def decline_request(self, from_user, to_user):
        try:
            friend_request = FriendRequestModel.objects.get(from_user=from_user, to_user=to_user)
        except FriendRequestModel.DoesNotExist:
            raise ValueError("Friend request not found")

        friend_request.status = FriendRequestModel.StatusModel.DECLINED
        friend_request.save()

    def accept_friend_request(self, to_user, from_user):
        """
        to_user — тот, кто принимает (request.user),
        from_user — тот, кто отправил заявку.
        """
        try:
            friend_request = FriendRequestModel.objects.get(from_user=from_user, to_user=to_user)
        except FriendRequestModel.DoesNotExist:
            raise ValidationError("Friend request not found")

        # Сортировка пользователей по id
        user1, user2 = sorted([to_user, from_user], key=lambda u: u.id)

        if FriendShipModel.objects.filter(user1=user1, user2=user2).exists():
            raise ValidationError("Already friends")

        FriendShipModel.objects.create(user1=user1, user2=user2)
        friend_request.delete()

    def send_friend_request(self, from_user, to_user):
        if from_user == to_user:
            raise ValueError("Нельзя добавить себя в друзья")

        existing = FriendRequestModel.objects.filter(
            (Q(from_user=from_user) & Q(to_user=to_user)) | (Q(from_user=to_user) & Q(to_user=from_user))
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

    def is_friends(self, user_a, user_b) -> bool:
        """Проверяет, друзья ли два пользователя."""
        return FriendShipModel.objects.filter(Q(user1=user_a, user2=user_b) | Q(user1=user_b, user2=user_a)).exists()

    def get_friends(self, user):
        """Возвращает всех друзей пользователя."""
        friendships = FriendShipModel.objects.filter(Q(user1=user) | Q(user2=user))
        friends = []
        for friendship in friendships:
            if friendship.user1 == user:
                friends.append(friendship.user2)
            else:
                friends.append(friendship.user1)
        return friends


class BlockService:
    pass
