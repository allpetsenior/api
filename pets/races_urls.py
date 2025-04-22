from django.urls import path

from pets.views.PetRacesView import PetRaces

urlpatterns = [
    path("", PetRaces.as_view())
]
