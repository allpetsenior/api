from core.models import Invite


class Invite_Repository():
  def create_invite(self, data):
    return Invite.objects.create(**data)
