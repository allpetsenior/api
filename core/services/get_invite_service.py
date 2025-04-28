from core.repositories.invite_repository import Invite_Repository
from v0.errors.app_error import App_Error

repo = Invite_Repository()


def get_invite_service(data):
  if data is None:
    raise App_Error(
        "ERROR:GET_USER_BY_USERNAME_SERVICE - params is is required", 400)

  return {"invite": repo.find_invite(data)}
