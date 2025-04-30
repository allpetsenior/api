from django.urls import path
from ai.views.prompt_pet_recommendations_view import PromptPetRecommendations
from ai.views.get_user_chat_view import GetUserChat
from ai.views.feedback_recommendation_view import FeedbackView

urlpatterns = [
    path("/prompt/pet/recommendations", PromptPetRecommendations.as_view()),
    path("/recommendation/<str:recommendation_id>/feedback", FeedbackView.as_view()),
    path("/chat", GetUserChat.as_view())
]
