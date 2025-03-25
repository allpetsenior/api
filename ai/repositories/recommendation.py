from ai.models import Recommendation
from v0.errors.app_error import App_Error


class RecommendationRepository():
    @staticmethod
    def validate_creation(data):
        if "type" not in data:
            raise App_Error("Recommendation.type is require", 400)
        if "content" not in data:
            raise App_Error("Recommendation.content is require", 400)
        if "update_in" not in data:
            raise App_Error("Recommendation.update_in is require", 400)
        if "pet" not in data:
            raise App_Error("Recommendation.pet is require", 400)

    def create(self, data):
        self.validate_creation(data)

        return Recommendation.objects.create(**data)

    def create_many(self, data):
        arr = []
        for item in data:
            self.validate_creation(item)
            arr.append(Recommendation(**item))

        return Recommendation.objects.bulk_create(arr)

    def update_or_create(self, data):
        self.validate_creation(data)

        return Recommendation.objects.update_or_create(**data)

    def get(self, data):
        return Recommendation.objects.get(**data)

    def filter(self, data):
        return Recommendation.objects.filter(**data)
