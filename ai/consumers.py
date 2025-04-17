import traceback
from channels.generic.websocket import JsonWebsocketConsumer
from ai.chatbot_provider import Chatbot
from ai.services.get_or_create_user_chat_service import get_or_create_user_chat
from v0.errors.app_error import App_Error
from ai.serializers import ChatSerializer
from concurrent.futures import ThreadPoolExecutor

chatbot = Chatbot()


class ChatConsumer(JsonWebsocketConsumer):
    def connect(self):
        try:
            user = self.scope["user"]
            if user.is_anonymous:
                self.close()

            self.accept()

            finded_chat = get_or_create_user_chat({"user": user})
            res = chatbot.send_message(messages=[
                {"content": "OPEN-CONNECTION", "role": "user"}])

            if not "data" in finded_chat:
                raise App_Error(
                    "User_chat was not created or finded", 404)

            serializer = ChatSerializer(finded_chat["data"])
            self.send_json(content={
                "content": res["data"], "role": "assistant", "chat": serializer.data})
        except Exception as e:
            print("ERROR-CHAT_CONSUMER")
            traceback.print_exception(e)
            self.close()

    def disconnect(self, code):
        self.close(code)

    def receive_json(self, content, **_):
        res = chatbot.send_message(messages=content)
        self.send_json(
            content={"content": res["data"], "role": "assistant"})
