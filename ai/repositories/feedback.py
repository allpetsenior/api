from ai.models import Feedback


class FeedbackRepository():
    def create_recommendation_feedback(self, data):
        return Feedback.objects.create(**data)

    def get_feedback_by_recommendation_id(self, recommendation_id):
        try:
            return Feedback.objects.get(recommendation__id=recommendation_id)
        except Feedback.DoesNotExist:
            return None
