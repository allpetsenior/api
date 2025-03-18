from core.repositories.feedback_repository import Feedback_Repository
from v0.errors.app_error import App_Error

repo = Feedback_Repository()


def validate(data):
  if "email" not in data:
    raise App_Error("Feedback.email is required", 400)


def create_feedback_service(data):
  validate(data)

  feedback = repo.create_feedback(data)

  return {"feedback": feedback}
