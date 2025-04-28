from django.db import IntegrityError

from core.models import Action
from v0.errors.app_error import App_Error


class Action_Repository():
  def create_action(self, data):
    try:
      return Action.objects.create(**data)

    except IntegrityError as e:
      raise App_Error(
          f'INTEGRITY_ERROR USER_REPOSITORY_CREATE_USER {str(e)}', 500)
