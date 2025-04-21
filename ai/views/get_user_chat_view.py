import traceback

from rest_framework.views import APIView
from rest_framework.response import Response
from django.views.decorators.vary import vary_on_headers
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from rest_framework.permissions import IsAuthenticated
from ai.services.get_user_chat_service import get_user_chat
from ai.serializers import ChatSerializer
from v0.errors.app_error import App_Error


class GetUserChat(APIView):
    permission_classes = [IsAuthenticated]

    @method_decorator(cache_page(60 * 60 * 24))
    @method_decorator(vary_on_headers("Authorization"))
    def get(self, request):
        try:
            chat = get_user_chat({"user": request.user})

            serializer = ChatSerializer(chat)

            return Response({"data": {"chat": serializer.data}})
        except App_Error as e:
            traceback.print_exception(e)
            return Response(e.toHttp(), e.status)
        except Exception as e:
            traceback.print_exception(e)
            return Response({"error": {"message": str(e)}}, 500)
