from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.views.generic import TemplateView

from messaging.models import ChatGroup, GroupMessage


class ChatView(TemplateView):
    template_name = "chat.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Берём room_name из URL (chat/<room_name>/)
        room_name = self.kwargs.get("room_name")

        # Ищем чат по этому имени или 404 если его нет
        chatroom = get_object_or_404(ChatGroup, group_name=room_name)

        # Берём сообщения (самые свежие последние)
        messages = GroupMessage.objects.filter(group=chatroom).order_by("-created_at")

        # Добавляем всё в контекст
        context.update(
            {
                "room_name": room_name,  # чтобы можно было вставлять {{ room_name }}
                "chatroom": chatroom,  # для твоего кода
                "chat_group": chatroom,  # алиас, чтобы шаблон видел chat_group.*
                "chat_messages": messages,  # сами сообщения
                "other_user": None,  # заглушка для приватных чатов (пока нет логики)
            }
        )

        return context


def edit_chatroom(request, group_name):
    return HttpResponse(f"Редактирование комнаты {group_name} (заглушка)")


def chat_file_upload(request, group_name):
    return HttpResponse(f"Файл загружен в {group_name} (заглушка)")


def chatroom_leave(request, group_name):
    return HttpResponse(f"Вышли из комнаты {group_name} (заглушка)")


# def chat_file_upload(request, group_name):
#     # Пока заглушка — позже можно будет сделать загрузку файлов
#     return JsonResponse({"status": "ok"})
