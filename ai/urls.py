from django.urls import path
from ai.views.chat_view import ChatView

urlpatterns = [
    path("/chat", ChatView.as_view()),
]
