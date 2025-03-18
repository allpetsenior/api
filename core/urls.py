from django.urls import path

from core.views.create_feedback_view import create_feedback_view
from core.views.create_invite_view import create_invite_view
from core.views.create_user_view import create_user_view
from core.views.login_view import login_view

urlpatterns = [
    path("/user", create_user_view),
    path("/login", login_view),
    path("/invites", create_invite_view),
    path("/feedbacks", create_feedback_view),
]
