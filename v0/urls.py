from django.urls import path, include

urlpatterns = [
    path("/core", include("core.urls")),
    path("/pet", include("pets.pet_urls")),
    path("/pets", include("pets.pets_urls")),
    path("/ai", include("ai.urls")),
    path("/age-calculator", include("pets.age_calculator_urls")),
    path("/races", include("pets.races_urls")),
    path("/analytics", include("analytics.urls")),
]
