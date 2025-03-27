from pets.models import PetAge


class PetAgeRepository():
    def get_ages(self):
        return PetAge.objects.all()
