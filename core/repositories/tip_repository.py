from core.models import Tip


class Tip_Repository():
  def find_tip(self, data):
    try:
      return Tip.objects.filter(**data)
    except Tip.DoesNotExist:
      return None
