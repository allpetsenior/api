from core.models import Feedback


class Feedback_Repository():
  def create_feedback(self, data):
    return Feedback.objects.create(**data)
