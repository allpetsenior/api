from ai.repositories.recommendation import RecommendationRepository

recommendation_repo = RecommendationRepository()


def create_many_recommendations_service(data):
    recommendation_repo.create_many(data)
