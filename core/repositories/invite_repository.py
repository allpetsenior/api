from core.models import Invite


class Invite_Repository():
  def create_invite(self, data):
    return Invite.objects.create(**data)

  def find_invite(self, data):
    try:
      return Invite.objects.get(**data)
    except Invite.DoesNotExist:
      return None
