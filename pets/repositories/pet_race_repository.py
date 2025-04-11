from pets.models import PetRace


class PetRaceRepository():
  def get_race(self, data):
    return PetRace.objects.filter(**data)
