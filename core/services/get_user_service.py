from core.repositories.user_repository import User_Repository
from v0.errors.app_error import App_Error

repo = User_Repository()


def get_user_service(data):
    if data is None:
        raise App_Error(
            "ERROR:GET_USER_BY_USERNAME_SERVICE - params is is required", 400)

    return {"user": repo.find_user(data)}
