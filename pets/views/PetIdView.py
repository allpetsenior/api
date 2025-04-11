import traceback

from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from pets.services.delete_pet_service import delete_pet_service
from pets.services.update_pet_service import update_pet_service
from v0.errors.app_error import App_Error


class PetIdView(APIView):
  permission_classes = [IsAuthenticated]

  def put(self, request, pet_id):
    try:
      data_to_insert = request.data["data"]
      query = {"id": pet_id, "tutor": request.user}
      updated_pet = update_pet_service(query, data_to_insert)

      if "error" in updated_pet:
        print(updated_pet["error"])
        return Response({"error": {"message": str(updated_pet["error"])}}, 500)

      return Response({"data": updated_pet["data"]}, 200)

    except App_Error as e:
      traceback.print_exception(e)
      return Response(e.toHttp(), e.status)
    except Exception as e:
      traceback.print_exception(e)
      return Response({"error": {"message": str(e)}}, 500)

  def delete(self, request, pet_id):
    try:
      query = {"id": pet_id, "tutor": request.user}
      delete_pet = delete_pet_service(query)

      if "error" in delete_pet:
        print(delete_pet["error"])
        return Response({"error": {"message": str(delete_pet["error"])}}, 500)

      return Response({"data": delete_pet["data"]}, 200)

    except App_Error as e:
      traceback.print_exception(e)
      return Response(e.toHttp(), e.status)
    except Exception as e:
      traceback.print_exception(e)
      return Response({"error": {"message": str(e)}}, 500)
