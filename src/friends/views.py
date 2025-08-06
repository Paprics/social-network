from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import ValidationError
from django.http.response import JsonResponse
from django.shortcuts import get_object_or_404, redirect
from django.views.generic.base import View

from .services import FriendService

User = get_user_model()

# Отправить - Отменить - Отклонить(смена статуса) - подтвердить - удалить


class SendFriendRequestView(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        to_user_id = request.POST.get("to_user_id")
        if not to_user_id or not to_user_id.isdigit():
            return JsonResponse({"error": "Invalid to_user_id"}, status=400)

        to_user_id = int(to_user_id)
        from_user = request.user
        to_user = get_object_or_404(User, pk=to_user_id)

        service = FriendService()
        try:
            service.send_friend_request(from_user, to_user)
        except ValueError as e:
            return JsonResponse({"error": str(e)}, status=400)

        # Всё успешно — редирект обратно на ту страницу, с которой пришёл
        return redirect(request.META.get("HTTP_REFERER", "/"))


# Retract request
class RetractFriendRequestView(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        to_user_id = request.POST.get("to_user_id")
        if not to_user_id or not to_user_id.isdigit():
            return JsonResponse({"error": "Invalid to_user_id"}, status=400)

        to_user_id = int(to_user_id)
        from_user = request.user
        to_user = get_object_or_404(User, pk=to_user_id)

        service = FriendService()
        try:
            service.retract_friend_request(from_user, to_user)
        except ValueError as e:
            return JsonResponse({"error": str(e)}, status=400)

        return redirect(request.META.get("HTTP_REFERER", "/"))


class DeclineFriendRequestView(LoginRequiredMixin, View): ...


class AcceptFriendRequestView(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        to_user_id = request.POST.get("to_user_id")

        try:
            to_user_id = int(to_user_id)
        except (TypeError, ValueError):
            return JsonResponse({"error": "Invalid to_user_id"}, status=400)

        from_user = request.user
        to_user = get_object_or_404(User, pk=to_user_id)

        service = FriendService()
        try:
            service.accept_friend_request(from_user, to_user)
        except ValidationError as e:
            return JsonResponse({"error": str(e)}, status=400)

        return redirect(request.META.get("HTTP_REFERER", "/"))


class RemoveFriendView(LoginRequiredMixin, View): ...
