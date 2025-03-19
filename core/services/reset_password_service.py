from core.repositories.user_repository import User_Repository

user_repo = User_Repository()


def reset_user_password_service(query, data):
    return user_repo.update(query, data)
