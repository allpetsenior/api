from pets.models import Pet
from v0.errors.app_error import App_Error


def update_pet_service(query, data):
    try:
        affected_rows = Pet.objects.filter(**query).update(**data)

        if affected_rows == 0:
            raise App_Error("Pet not founded", 404)

        return {"data": affected_rows}
    except Exception as e:
        return {"error": e}
