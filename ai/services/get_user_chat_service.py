from ai.models import Chat
from ai.repositories.chat import ChatRepository
from v0.errors.app_error import App_Error

chat_repo = ChatRepository()


def get_user_chat(data):
    try:
        chat = chat_repo.get_chat_by_user(user=data["user"])
        return chat
    except Chat.DoesNotExist:
        raise App_Error("ERROR-GET-USER-CHAT: Query does not exist", 404)
