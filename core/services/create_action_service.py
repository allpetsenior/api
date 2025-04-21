from core.repositories.action_repository import Action_Repository
from v0.errors.app_error import App_Error

repo = Action_Repository()


def create_action_service(data):
  if data is None:
    raise App_Error(
        "ERROR:CREATE_ACTION_SERVICE - params is is required", 400)

  return {"data": repo.create_action(data)}
