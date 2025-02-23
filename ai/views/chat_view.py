import traceback
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from v0.errors.app_error import App_Error
from ai.chatbot_provider import Chatbot

chatbot = Chatbot()


def validate(data):
    if "message" not in data:
        raise App_Error("request.body.message is required", status=400)


class ChatView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            validate(request.data)

            messages = request.data["message"]

            res = chatbot.send_message(messages=messages)

            return Response(res, status=res["status"])

        except App_Error as e:
            traceback.print_exception(e)
            return Response(e.toHttp(), e.status)
        except Exception as e:
            traceback.print_exception(e)
            return Response({"error": {"message": str(e)}}, 500)
