from pets.repositories.pet_repository import PetRepository
from v0.errors.app_error import App_Error

pet_repo = PetRepository()


def validate(data):
    if "name" not in data:
        raise App_Error("pet.name is required", 400)
    if "race" not in data:
        raise App_Error("pet.race is required", 400)
    """if "size" not in data:
        raise App_Error("pet.size is required", 400)
        """
    if "activity" not in data:
        raise App_Error("pet.activity is required", 400)
    if "health_problem" not in data:
        raise App_Error("pet.health_problem is required", 400)
    if "birth_date" not in data:
        raise App_Error("pet.birth_date is required", 400)
    if "weight" not in data:
        raise App_Error("pet.weight is required", 400)
    if "tutor" not in data:
        raise App_Error("pet.tutor is required", 400)


def create_many_pets_service(data):
    if type(data) != list:
        raise App_Error(
            "ERROR CREATE_MANY_PETS_SERVICE - Data must be a list", 400)

    for item in data:
        validate(item)

    return {"data": pet_repo.create_many_pets(data)}
