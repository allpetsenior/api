from django.urls import path
from pets.views.PetsIndexView import IndexView

urlpatterns = [
    path("", IndexView.as_view()),
]
