from pets.repositories.pet_race_repository import PetRaceRepository

repo = PetRaceRepository()


def get_pet_race_service(data):
    return {"data": repo.get_race(data)}
