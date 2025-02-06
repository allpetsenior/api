from v0.errors.app_error import App_Error
from core.repositories.token_repository import TokenRepository

repo = TokenRepository()


def get_token_by_user_service(user):
    if user is None:
        raise App_Error(
            "ERROR: GET_TOKEN_BY_USER_SERVICE - user is required", 400)

    return {"data": repo.get_token_by_user(user)}
