from ai.repositories.chat import ChatRepository

repo = ChatRepository()


def decrease_user_chat_monthly_message(data):
    data = repo.decrease_user_chat_monthly_message(data)

    return {"data": data}
