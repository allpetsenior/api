from ai.repositories.feedback import FeedbackRepository
from v0.errors.app_error import App_Error

feedback_repo = FeedbackRepository()


def create_feedback_recommendation_service(data):
    if "recommendation_id" not in data:
        raise App_Error(
            "CREATE-FEEDBACK-RECOMMENDATION-ERROR: Feedback.recommendation_id is required", 400)

    if "is_good" not in data:
        raise App_Error(
            "CREATE-FEEDBACK-RECOMMENDATION-ERROR: Feedback.is_good is required", 400)

    return feedback_repo.create_recommendation_feedback(data)
