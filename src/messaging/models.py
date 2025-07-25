from django.contrib.auth import get_user_model
from django.db import models

USER = get_user_model()


class ChatGroup(models.Model):
    group_name = models.CharField(max_length=128, unique=True)

    def __str__(self):
        return self.group_name

    class Meta:
        verbose_name = "Chat Group"
        verbose_name_plural = "Chat Groups"


class GroupMessage(models.Model):
    group = models.ForeignKey(ChatGroup, related_name="messages", on_delete=models.CASCADE)
    author = models.ForeignKey(USER, on_delete=models.CASCADE)
    body = models.CharField(max_length=300)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.author} : {self.body}"

    class Meta:
        verbose_name = "Group Message"
        verbose_name_plural = "Group Messages"
        ordering = ["-created_at"]
