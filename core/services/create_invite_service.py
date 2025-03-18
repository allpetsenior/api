from core.repositories.invite_repository import Invite_Repository
from v0.errors.app_error import App_Error

repo = Invite_Repository()


def validate(data):
  if "email" not in data:
    raise App_Error("Invite.email is required", 400)


def create_invite_service(data):
  validate(data)

  invite = repo.create_invite(data)

  return {"invite": invite}
