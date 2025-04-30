from ai.repositories.feedback import FeedbackRepository
from v0.errors.app_error import App_Error

feedback_repo = FeedbackRepository()


def get_feedback_by_recommendation_id(recommendation_id):
    if "recommendation_id" is None:
        raise App_Error(
            "GET-FEEDBACK-RECOMMENDATION-ERROR: recommendation_id is required", 400)

    return feedback_repo.get_feedback_by_recommendation_id(recommendation_id)
