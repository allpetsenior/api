from datetime import timedelta
from django.utils import timezone
from ai.repositories.chat import ChatRepository

repo = ChatRepository()


def reset_chat_messages(data):
    chat = repo.get_chat_by_user(data["user"])

    chat.remaining_messages = chat.max_messages
    chat.reset_in = timezone.now() + timedelta(days=30)

    chat.save()

    return {"data": chat}
