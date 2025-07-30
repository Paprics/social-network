import json

from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
from django.contrib.auth import get_user_model
from django.template.loader import render_to_string

from .models import ChatGroup, GroupMessage

User = get_user_model()


class ChatroomConsumer(WebsocketConsumer):
    def connect(self):
        user_lazy = self.scope["user"]
        self.user = user_lazy._wrapped if hasattr(user_lazy, "_wrapped") else user_lazy

        self.chatroom_name = self.scope["url_route"]["kwargs"]["chatroom_name"]

        try:
            self.chatroom = ChatGroup.objects.get(group_name=self.chatroom_name)
        except ChatGroup.DoesNotExist:
            # Можно залогировать, если хочешь, или просто молча закрыть коннект
            self.close()  # аккуратно закрываем WS соединение
            return

        async_to_sync(self.channel_layer.group_add)(self.chatroom_name, self.channel_name)

        if self.user.is_authenticated:
            if self.user not in self.chatroom.users_online.all():
                self.chatroom.users_online.add(self.user)
                self.update_online_count()

        self.accept()

    def disconnect(self, close_code):
        async_to_sync(self.channel_layer.group_discard)(self.chatroom_name, self.channel_name)

        if self.user.is_authenticated:
            if self.user in self.chatroom.users_online.all():
                self.chatroom.users_online.remove(self.user)
                self.update_online_count()

    def receive(self, text_data):
        print("📥 RAW WebSocket DATA:", text_data)  # что реально пришло от клиента

        text_data_json = json.loads(text_data)
        body = text_data_json["message"]

        print("📦 Распарсенный JSON:", text_data_json)
        print("✍ Текст сообщения:", body)

        message = GroupMessage.objects.create(body=body, author=self.user, group=self.chatroom)
        print("✅ Сообщение сохранено в БД:", message)

        event = {
            "type": "message_handler",
            "message_id": message.id,
        }
        print("📤 Event для отправки в группу:", event)

        async_to_sync(self.channel_layer.group_send)(self.chatroom_name, event)

        print(f"📡 Event отправлен в WebSocket-группу [{self.chatroom_name}]")

    def message_handler(self, event):
        message_id = event["message_id"]
        message = GroupMessage.objects.get(id=message_id)
        context = {
            "message": message,
            "user": self.user,
            "chat_group": self.chatroom,
        }

        html = render_to_string("includes/_chat_message.html", context)
        wrapped_html = f"<ul id='chat_messages' hx-swap-oob='beforeend'>{html}</ul>"
        self.send(text_data=wrapped_html)

    def update_online_count(self):
        online_count = self.chatroom.users_online.count() - 1

        event = {"type": "online_count_handler", "online_count": online_count}
        async_to_sync(self.channel_layer.group_send)(self.chatroom_name, event)

    def online_count_handler(self, event):
        online_count = event["online_count"]

        chat_messages = ChatGroup.objects.get(group_name=self.chatroom_name).chat_messages.all()[:30]
        author_ids = set([message.author.id for message in chat_messages])
        users = User.objects.filter(id__in=author_ids)

        context = {"online_count": online_count, "chat_group": self.chatroom, "users": users}
        html = render_to_string("includes/_online_count.html", context)
        self.send(text_data=html)


class OnlineStatusConsumer(WebsocketConsumer):
    def connect(self):
        self.user = self.scope["user"]
        self.group_name = "online-status"

        # 🛡️ Безопасно ищем "online-status", иначе делаем заглушку
        self.group, _ = ChatGroup.objects.get_or_create(
            group_name=self.group_name, defaults={"title": "Online Status System Chat", "is_private": False}
        )

        if self.user not in self.group.users_online.all():
            self.group.users_online.add(self.user)

        async_to_sync(self.channel_layer.group_add)(self.group_name, self.channel_name)

        self.accept()
        self.online_status()

    def disconnect(self, close_code):
        if self.user in self.group.users_online.all():
            self.group.users_online.remove(self.user)

        async_to_sync(self.channel_layer.group_discard)(self.group_name, self.channel_name)
        self.online_status()

    def online_status(self):
        event = {"type": "online_status_handler"}
        async_to_sync(self.channel_layer.group_send)(self.group_name, event)

    def online_status_handler(self, event):
        # 🔹 Кто онлайн (кроме текущего)
        online_users = self.group.users_online.exclude(id=self.user.id)

        # 🛡️ Пытаемся найти public-chat
        try:
            public_chat = ChatGroup.objects.get(group_name="public-chat")
            public_chat_users = public_chat.users_online.exclude(id=self.user.id)
        except ChatGroup.DoesNotExist:
            public_chat_users = ChatGroup.objects.none()

        # 🔹 Все чаты юзера
        my_chats = self.user.chat_groups.all()

        # 🛠 Приватные чаты с онлайновыми юзерами
        private_chats_with_users = [
            chat for chat in my_chats.filter(is_private=True) if chat.users_online.exclude(id=self.user.id)
        ]

        # 🛠 Групповые чаты (у тебя поле group_name, так что условие другое)
        group_chats_with_users = [
            chat for chat in my_chats.filter(is_private=False) if chat.users_online.exclude(id=self.user.id)
        ]

        online_in_chats = bool(public_chat_users or private_chats_with_users or group_chats_with_users)

        # 🔹 Формируем контекст
        context = {
            "online_users": online_users,
            "online_in_chats": online_in_chats,
            "public_chat_users": public_chat_users,
            "user": self.user,
        }

        # 🛠 Если шаблона нет – просто отправляем JSON
        try:
            html = render_to_string("includes/_online_status.html", context=context)
        except Exception:
            html = f"<div>⚠️ Online users: {online_users.count()}</div>"

        self.send(text_data=html)
