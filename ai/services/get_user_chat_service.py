from ai.repositories.chat import ChatRepository

chat_repo = ChatRepository()


def get_user_chat(data):
    chat, created = chat_repo.get_or_create_chat(data)
    if created:
        print(f"CREATED CHAT -> {data["user"].id}")
    return chat
