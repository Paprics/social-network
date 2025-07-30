from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import Http404, HttpResponse
from django.shortcuts import get_object_or_404, redirect
from django.views.generic import TemplateView
from django.views.generic.base import View

from messaging.models import ChatGroup, GroupMessage

User = get_user_model()


class GetOrCreateDialogView(LoginRequiredMixin, View):
    def get(self, request, username):
        if request.user.username == username:
            return redirect("main:index")

        other_user = get_object_or_404(User, username=username)
        # ищем приватный чат с этим пользователем
        private_chats = request.user.chat_groups.filter(is_private=True)

        chatroom = None
        for chat in private_chats:
            if other_user in chat.members.all():
                chatroom = chat
                break

        # если нет — создаём новый
        if not chatroom:
            chatroom = ChatGroup.objects.create(is_private=True)
            chatroom.members.add(request.user, other_user)

        # ✅ РЕДИРЕКТ НА ПРАВИЛЬНЫЙ URL (name="chat")
        return redirect("messaging:chat", room_name=chatroom.group_name)


class ChatView(TemplateView):
    template_name = "chat.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        room_name = self.kwargs.get("room_name")
        chatroom = get_object_or_404(ChatGroup, group_name=room_name)

        if chatroom.is_private:
            # Проверка, что текущий пользователь — участник диалога
            if self.request.user not in chatroom.members.all():
                raise Http404("You are not a member of this private chat")

            # Находим другого пользователя
            other_user = chatroom.members.exclude(id=self.request.user.id).first()
        else:
            other_user = None  # В публичном чате нет "другого" пользователя

        messages = GroupMessage.objects.filter(group=chatroom).order_by("-created_at")

        context.update(
            {
                "room_name": room_name,
                "chatroom": chatroom,
                "chat_group": chatroom,
                "chat_messages": messages,
                "other_user": other_user,
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
