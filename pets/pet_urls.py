from django.urls import path
from pets.views.PetIndexView import IndexView
from pets.views.PetIdView import PetIdView

urlpatterns = [
    path("", IndexView.as_view()),
    path("/<str:pet_id>", PetIdView.as_view()),
]
