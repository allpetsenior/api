from django.urls import path
from core.views.index_view import IndexView
from core.views.login_view import login_view

urlpatterns = [
    path("/user", IndexView.as_view()),
    path("/login", login_view)
]
