from ai.models import Recommendation
from ai.repositories.recommendation import RecommendationRepository

recommendation_repo = RecommendationRepository()


def update_or_create_recommendation_service(data):
    try:
        r = recommendation_repo.get({"pet": data["pet"], "type": data["type"]})

        r.update_in = data["update_in"]
        r.content = data["content"]

        print(
            f"UPDATED {data["type"].upper()} RECOMMENDATION -> Pet.id = {data["pet"].id}")

        r.save()
        return r
    except Recommendation.DoesNotExist:
        print(
            f"CREATE {data["type"].upper()} RECOMMENDATION -> Pet.id = {data["pet"].id}")
        return recommendation_repo.create(data)
