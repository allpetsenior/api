from pets.models import Pet
from pets.repositories.pet_race_repository import PetRaceRepository
from v0.errors.app_error import App_Error

pet_race_repo = PetRaceRepository()


def update_pet_service(query, data):
  try:
    if "race" in data:
      race = pet_race_repo.get_race(
          {"name": data["race"]["name"], 'specie': data['race']['specie']})
      data["race"] = race

    affected_rows = Pet.objects.filter(**query).update(**data)

    if affected_rows == 0:
      raise App_Error("Pet not founded", 404)

    return {"data": affected_rows}
  except Exception as e:
    return {"error": e}
