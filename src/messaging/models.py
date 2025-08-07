import shortuuid
from django.contrib.auth import get_user_model
from django.db import models

USER = get_user_model()


def generate_uuid():
    return shortuuid.uuid()


class ChatGroup(models.Model):
    group_name = models.CharField(max_length=128, unique=True, default=generate_uuid)
    title = models.CharField(max_length=128)
    admin = models.ForeignKey(
        USER,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="admin_of_groups"
    )
    members = models.ManyToManyField(USER, related_name="chat_groups", blank=True)
    users_online = models.ManyToManyField(USER, blank=True, related_name="online_groups")
    is_private = models.BooleanField(default=False)

    def __str__(self):
        return self.group_name

    def get_other_user(self, current_user):
        return self.members.exclude(id=current_user.id).first()

    class Meta:
        verbose_name = "Chat Group"
        verbose_name_plural = "Chat Groups"


class GroupMessage(models.Model):
    group = models.ForeignKey(ChatGroup, related_name="chat_messages", on_delete=models.CASCADE)
    author = models.ForeignKey(USER, on_delete=models.CASCADE)
    body = models.CharField(max_length=300)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.author}: {self.body}"

    class Meta:
        verbose_name = "Group Message"
        verbose_name_plural = "Group Messages"
        ordering = ["-created_at"]
