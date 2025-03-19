from core.repositories.feedback_repository import Feedback_Repository
from v0.errors.app_error import App_Error

repo = Feedback_Repository()


def create_feedback_service(data):
  feedback = repo.create_feedback(data)

  return {"feedback": feedback}
