from datetime import timedelta

from django.utils import timezone
from ai.models import Chat


class ChatRepository():
    def get_or_create_chat(self, data):
        data["reset_in"] = data["reset_in"] if "reset_in" in data else timezone.now() + \
            timedelta(days=30)
        chat = Chat.objects.get_or_create(user=data["user"], defaults=data)

        return chat

    def decrease_user_chat_monthly_message(self, data):
        chat = Chat.objects.get(user=data["user"])

        n = data["number"] if "number" in data else 1

        chat.remaining_messages -= n
        chat.save()

        return chat.remaining_messages

    def get_chat_by_user(self, user):
        chat = Chat.objects.get(user=user)

        return chat
