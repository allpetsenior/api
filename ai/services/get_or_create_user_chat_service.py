from ai.repositories.chat import ChatRepository

repo = ChatRepository()


def get_or_create_user_chat(data):
    (data, created) = repo.get_or_create_chat(data)
    return {"data": data, "created": created}
