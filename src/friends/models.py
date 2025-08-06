from django.conf import settings
from django.db import models

User = settings.AUTH_USER_MODEL


class FriendRequestModel(models.Model):
    from_user = models.ForeignKey(User, related_name="sent_requests", on_delete=models.CASCADE)
    to_user = models.ForeignKey(User, related_name="received_requests", on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class StatusModel(models.TextChoices):
        PENDING = "pending", "Pending"
        DECLINED = "declined", "Declined"

    status = models.CharField(max_length=10, choices=StatusModel.choices, default=StatusModel.PENDING)

    class Meta:
        unique_together = ("from_user", "to_user")
        db_table = "friends_request"

    def __str__(self):
        return f"{self.from_user} → {self.to_user} ({self.status})"


class FriendShipModel(models.Model):
    user1 = models.ForeignKey(User, related_name="friendship_user1", on_delete=models.CASCADE)
    user2 = models.ForeignKey(User, related_name="friendship_user2", on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("user1", "user2")
        db_table = "friend"

    def __str__(self):
        return f"{self.user1} ↔ {self.user2}"

    def save(self, *args, **kwargs):
        # Автосортировка: user1 всегда с меньшим id
        if self.user1.id > self.user2.id:
            self.user1, self.user2 = self.user2, self.user1
        super().save(*args, **kwargs)


class BlockModel(models.Model):
    blocker = models.ForeignKey(User, related_name="blocking", on_delete=models.CASCADE)
    blocked = models.ForeignKey(User, related_name="blocked_by", on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("blocker", "blocked")
        db_table = "blocked_users"

    def __str__(self):
        return f"{self.blocker} 🚫 {self.blocked}"
