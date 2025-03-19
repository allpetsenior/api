from django.urls import path
from core.views.index_view import IndexView
from core.views.login_view import login_view
from core.views.forgot_password_view import forgot_password_view

urlpatterns = [
    path("/user", IndexView.as_view()),
    path("/login", login_view),
    path("/forgot-password", forgot_password_view),
]
