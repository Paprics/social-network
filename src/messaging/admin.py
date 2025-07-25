from django.contrib import admin

from messaging.models import ChatGroup, GroupMessage


@admin.register(GroupMessage)
class GroupMessageAdmin(admin.ModelAdmin):
    list_display = ("author", "group", "created_at")
    search_fields = ("body", "author__username")
    list_filter = ("group", "created_at")


@admin.register(ChatGroup)
class ChatGroupAdmin(admin.ModelAdmin):
    list_display = ("group_name",)
    search_fields = ("group_name",)
