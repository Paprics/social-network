from django.shortcuts import get_object_or_404, redirect, render
from django.views import View

from messaging.forms import ChatMessageCreateForm
from messaging.models import ChatGroup


class ChatView(View):
    form_class = ChatMessageCreateForm
    template_name = "chat-2.html"

    def get(self, request):
        group = get_object_or_404(ChatGroup, group_name="public")
        messages = group.messages.order_by("created_at")[:30]
        form = self.form_class()
        return render(
            request,
            self.template_name,
            {
                "chat_messages": messages,
                "form": form,
                "group": group,
            },
        )

    def post(self, request):
        form = self.form_class(request.POST)
        group = get_object_or_404(ChatGroup, group_name="public")
        if form.is_valid():
            message = form.save(commit=False)
            message.author = request.user
            message.group = group
            message.save()
            return redirect(request.path)
        return render(
            request,
            self.template_name,
            {
                "chat_messages": group.messages.order_by("-created_at")[:30],
                "form": form,
                "group": group,
            },
        )
