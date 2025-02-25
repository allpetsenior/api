from django.urls import path
from ai.views.prompt_pet_recommendations_view import PromptPetRecommendations

urlpatterns = [
    path("/prompt/pet/recommendations", PromptPetRecommendations.as_view()),

]
