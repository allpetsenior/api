from pets.repositories.pet_age_repository import PetAgeRepository

pet_age_repo = PetAgeRepository()


def get_pet_ages_service():
    return pet_age_repo.get_ages()
