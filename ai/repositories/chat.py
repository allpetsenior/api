from datetime import timedelta, datetime
from ai.models import Chat


class ChatRepository():
    def get_or_create_chat(self, data):
        data["reset_in"] = data["reset_in"] if "reset_in" in data else datetime.now() + \
            timedelta(days=60)
        chat = Chat.objects.get_or_create(user=data["user"], defaults=data)

        return chat
