from django.urls import path, include

urlpatterns = [
    path("/core", include("core.urls")),
    path("/pet", include("pets.pet_urls")),
    path("/pets", include("pets.pets_urls")),
    path("/ai", include("ai.urls"))
]
