from ai.models import Recommendation
from ai.repositories.recommendation import RecommendationRepository

recommendation_repo = RecommendationRepository()


def update_or_create_recommendation_service(data):
    try:
        r = recommendation_repo.get({"pet": data["pet"], "type": data["type"]})

        r.update_in = data["update_in"]
        r.content = data["content"]

        print("UPDATED RECOMMENDATION")

        r.save()
        return r
    except Recommendation.DoesNotExist:
        print("CREATE RECOMMENDATION")
        return recommendation_repo.create(data)
