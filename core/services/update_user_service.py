from v0.errors.app_error import App_Error
from core.repositories.user_repository import User_Repository

user_repo = User_Repository()


def validate(data):
    if "id" in data:
        raise App_Error("user.id is not allowed to be updated", 400)


def update_user_service(query, data):
    validate(data)

    return user_repo.update(query, data)
