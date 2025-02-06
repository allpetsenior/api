from django.urls import path
from pets.views.PetIndexView import IndexView

urlpatterns = [
    path("", IndexView.as_view()),
]
