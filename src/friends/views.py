from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import ValidationError
from django.db.models.query_utils import Q
from django.http.response import HttpResponseBadRequest, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.views.generic.base import View

from .models import BlockedUserModel, FriendRequestModel, FriendShipModel
from .services import FriendService

User = get_user_model()


# Remove request
class RemoveFriendRequestView(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        target_user_id = request.POST.get("target_user_id")

        if not target_user_id or not target_user_id.isdigit():
            return JsonResponse({"error": "Invalid target_user_id"}, status=400)

        target_user = get_object_or_404(User, id=int(target_user_id))
        current_user = request.user

        service = FriendService()
        try:
            service.remove_friend(user_a=current_user, user_b=target_user)
            return redirect(request.META.get("HTTP_REFERER", "/"))
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)


# Chenge status request
class DeclineFriendRequestView(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        from_user_id = request.POST.get("from_user_id")

        if not from_user_id or not from_user_id.isdigit():
            return JsonResponse({"error": "Invalid from_user_id"}, status=400)

        from_user = get_object_or_404(User, id=int(from_user_id))
        to_user = request.user

        service = FriendService()
        try:
            service.decline_request(from_user, to_user)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)

        return redirect(request.META.get("HTTP_REFERER", "/"))


# Send request
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


# Accept request
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


class FriendsDetailView(View):
    template_name = "friends_requests_detail.html"

    def get(self, request, *args, **kwargs):
        user = request.user

        # Друзья — ищем по обеим колонкам
        friendships = FriendShipModel.objects.filter(Q(user1=user) | Q(user2=user))
        friends = [fs.user2 if fs.user1 == user else fs.user1 for fs in friendships]

        # Входящие заявки
        incoming_requests = FriendRequestModel.objects.filter(to_user=user)

        # Исходящие заявки
        outgoing_requests = FriendRequestModel.objects.filter(from_user=user)

        # Все заявки (входящие и исходящие)
        related_user_ids = set()
        related_user_ids.update(req.from_user.id for req in incoming_requests)
        related_user_ids.update(req.to_user.id for req in outgoing_requests)
        related_user_ids.update(friend.id for friend in friends)

        # Новые пользователи, которым можно отправить заявку
        suggestions = User.objects.exclude(id=user.id).exclude(id__in=related_user_ids)

        context = {
            "friends": friends,
            "incoming_requests": incoming_requests,
            "outgoing_requests": outgoing_requests,
            "suggestions": suggestions,
        }
        return render(request, self.template_name, context)


class BlockUserView(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        target_user_id = request.POST.get("user_id")
        if not target_user_id:
            return HttpResponseBadRequest("User ID not provided")

        target_user = get_object_or_404(User, pk=target_user_id)

        if target_user.id == request.user.id:
            return HttpResponseBadRequest("You cannot block yourself")

        BlockedUserModel.objects.get_or_create(blocker=request.user, blocked=target_user)

        return redirect(request.META.get("HTTP_REFERER", "/"))


class UnblockUserView(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        target_user_id = request.POST.get("user_id")
        if not target_user_id:
            return HttpResponseBadRequest("User ID not provided")

        target_user = get_object_or_404(User, pk=target_user_id)

        BlockedUserModel.objects.filter(blocker=request.user, blocked=target_user).delete()

        return redirect(request.META.get("HTTP_REFERER", "/"))
