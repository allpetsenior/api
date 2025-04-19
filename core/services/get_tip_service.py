from core.repositories.tip_repository import Tip_Repository
from v0.errors.app_error import App_Error

repo = Tip_Repository()


def get_tip_service(data):
  if data is None:
    raise App_Error(
        "ERROR:GET_USER_BY_USERNAME_SERVICE - params is is required", 400)

  return {"data": repo.find_tip(data)}
