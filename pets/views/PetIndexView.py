import traceback

from rest_framework.views import APIView
from rest_framework.response import Response
from pets.services.create_pet_service import create_pet_service
from rest_framework.permissions import IsAuthenticated
from pets.serializers.pet_serializer import PetSerializer
from v0.errors.app_error import App_Error


class IndexView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            pet = create_pet_service({**request.data, "tutor": request.user})

            serializer = PetSerializer(pet["data"])

            return Response({"data": serializer.data}, 201)

        except App_Error as e:
            traceback.print_exception(e)
            return Response(e.toHttp(), e.status)
        except Exception as e:
            traceback.print_exception(e)
            return Response({"error": {"message": str(e)}}, 500)
