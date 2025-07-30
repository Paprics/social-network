from django.contrib.auth import get_user_model

from messaging.models import ChatGroup

User = get_user_model()


def chats_processor(request):
    """Единый контекст-процессор для публичных чатов и приватных диалогов"""
    dialogs = []
    public_rooms = ChatGroup.objects.filter(is_private=False)

    if request.user.is_authenticated:
        private_chats = request.user.chat_groups.filter(is_private=True)
        for chat in private_chats:
            other_user = chat.members.exclude(id=request.user.id).first()
            dialogs.append({"chat": chat, "other_user": other_user})
    else:
        private_chats = []

    return {"chatrooms": public_rooms, "dialogs": dialogs}
