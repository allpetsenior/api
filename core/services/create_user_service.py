from core.repositories.user_repository import User_Repository
from v0.errors.app_error import App_Error

repo = User_Repository()


def validate(data):
    if "name" not in data:
        raise App_Error("User.name is required", 400)

    if "username" not in data:
        raise App_Error("User.username is required", 400)

    if "last_name" not in data:
        raise App_Error("User.last_name is required", 400)

    if "birth_date" not in data:
        raise App_Error("User.birth_date is required", 400)

    if "state" not in data:
        raise App_Error("User.state is required", 400)

    if "cellphone" not in data:
        raise App_Error("User.cellphone is required", 400)

    if "email" not in data:
        raise App_Error("User.email is required", 400)

    if "password" not in data:
        raise App_Error("User.password is required", 400)


def create_user_service(data):
    validate(data)

    user = repo.create_user(data)

    return {"user": user}
