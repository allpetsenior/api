import traceback

from datetime import datetime
from channels.generic.websocket import JsonWebsocketConsumer
from ai.chatbot_provider import Chatbot
from ai.services.get_or_create_user_chat_service import get_or_create_user_chat
from v0.errors.app_error import App_Error
from ai.serializers import ChatSerializer
from ai.services.decrease_user_chat_monthly_message_service import decrease_user_chat_monthly_message
from ai.services.reset_chat_messages_service import reset_chat_messages

chatbot = Chatbot()


class ChatConsumer(JsonWebsocketConsumer):
    def connect(self):
        try:
            user = self.scope["user"]
            if user.is_anonymous:
                self.close()
                return

            self.accept()

            finded_chat = get_or_create_user_chat({"user": user})

            if not "data" in finded_chat:
                raise App_Error(
                    "User_chat was not created or finded", 404)

            # Check if the current timestamp is greater than the reset timestamp
            if datetime.now().timestamp() > finded_chat["data"].reset_in.timestamp():
                # Reset chat messages if the condition is met
                reseted_chat = reset_chat_messages({"user": user})
                serializer = ChatSerializer(reseted_chat["data"])
                return self.send_json(content={
                    "content": "Olá, sou o assistente virtual da AllPetSenior. Como posso ajudar?", "role": "assistant", "chat": serializer.data})

            # Check if the remaining messages are less than or equal to zero
            if finded_chat["data"].remaining_messages <= 0:
                raise App_Error("Remaining messages is over", 400)

            self.send_json(content={
                "content": "Olá, sou o assistente virtual da AllPetSenior. Como posso ajudar?", "role": "assistant", "remaining_messages": finded_chat["data"].remaining_messages})
        except Exception as e:
            print("ERROR-CHAT_CONSUMER")
            traceback.print_exception(e)
            self.close()

    def disconnect(self, code):
        self.close(code)

    def receive_json(self, content, **_):
        user = self.scope["user"]
        res = chatbot.send_message(messages=content)
        remaining_messages = decrease_user_chat_monthly_message({"user": user})

        self.send_json(
            content={"content": res["data"], "role": "assistant", "remaining_messages": remaining_messages["data"]})

        if remaining_messages["data"] <= 0:
            self.close()
