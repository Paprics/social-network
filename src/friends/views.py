from django.contrib.auth import get_user_model
from django.http.response import JsonResponse, HttpResponseBadRequest, Http404
from django.shortcuts import render, get_object_or_404
from django.views.generic.base import View
from .services import FriendService
User = get_user_model()



class SendFriendRequestView(View):
    def post(self, request, *args, **kwargs):
        try:
            to_user_id = int(request.POST.get('to_user_id'))
            from_user = request.user
            to_user = get_object_or_404(User, pk=to_user_id)

            service = FriendService()
            service.send_friend_request(from_user, to_user)

        except ValueError as e:
            return JsonResponse({"error": str(e)}, status=400)
        except Http404:
            return JsonResponse({"error": "Пользователь не найден"}, status=404)

        return JsonResponse({"status": "success"})


