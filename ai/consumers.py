from channels.generic.websocket import JsonWebsocketConsumer
from ai.chatbot_provider import Chatbot

chatbot = Chatbot()


class ChatConsumer(JsonWebsocketConsumer):
    def connect(self):
        if self.scope["user"].is_anonymous:
            self.close()
        res = chatbot.send_message(
            messages=[{"content": "OPEN-CONNECTION", "role": "user"}])
        self.accept()
        self.send_json(content={"content": res["data"], "role": "assistant"})

    def disconnect(self, close_code):
        self.close(close_code)

    def receive_json(self, content):
        res = chatbot.send_message(messages=content)
        self.send_json(
            content={"content": res["data"], "role": "assistant"})
