from django.urls import path
from analytics.views import IndexView

urlpatterns = [
    path("", IndexView.as_view()),
]
