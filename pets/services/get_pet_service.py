from pets.repositories.pet_repository import PetRepository

pet_repo = PetRepository()


def get_pet_service(data):
    return {"data": pet_repo.get_pet(data)}
