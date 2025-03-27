from django.urls import path

from pets.views.AgeCalculatorView import AgeCalculatorView

urlpatterns = [
    path("", AgeCalculatorView.as_view())
]
