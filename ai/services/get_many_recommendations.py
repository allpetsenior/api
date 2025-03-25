from ai.repositories.recommendation import RecommendationRepository

recommendation_repo = RecommendationRepository()


def get_many_recommendations_service(data):
    return recommendation_repo.filter(
        data)
