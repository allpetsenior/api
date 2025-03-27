from django.urls import path
from pets.views.PetIndexView import IndexView
from pets.views.PetIdView import PetIdView

from pets.views.AgeCalculatorView import AgeCalculatorView
urlpatterns = [
    path("", IndexView.as_view()),
    path("/<str:pet_id>", PetIdView.as_view()),
    path("/age-calculator", AgeCalculatorView.as_view())
]
