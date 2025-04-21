from django.urls import path
from ai.views.prompt_pet_recommendations_view import PromptPetRecommendations
from ai.views.get_user_chat_view import GetUserChat

urlpatterns = [
    path("/prompt/pet/recommendations", PromptPetRecommendations.as_view()),
    path("/chat", GetUserChat.as_view())
]
