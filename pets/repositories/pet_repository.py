from pets.models import Pet


class PetRepository():
    def create_pet(self, data):
        return Pet.objects.create(**data)

    def get_pets(self, data):
        return Pet.objects.filter(**data)

    def get_pet(self, data):
        return Pet.objects.get(**data)

    def create_many_pets(self, data):
        pets = []
        for item in data:
            pets.append(Pet(**item))

        return Pet.objects.bulk_create(pets)
