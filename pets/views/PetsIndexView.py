import traceback

from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from pets.serializers.pet_serializer import PetSerializer
from pets.services.create_many_pets_service import create_many_pets_service
from pets.services.get_pets_service import get_pets_service
from v0.errors.app_error import App_Error


class IndexView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            pet = create_many_pets_service(
                [{**item, "tutor": request.user} for item in request.data])

            serializer = PetSerializer(pet["data"], many=True)

            return Response({"data": serializer.data}, 201)

        except App_Error as e:
            traceback.print_exception(e)
            return Response(e.toHttp(), e.status)
        except Exception as e:
            traceback.print_exception(e)
            return Response({"error": {"message": str(e)}}, 500)

    def get(self, request):
        try:
            pet = get_pets_service({**request.data, "tutor": request.user})

            serializer = PetSerializer(pet["data"], many=True)

            return Response({"data": serializer.data}, 200)

        except App_Error as e:
            traceback.print_exception(e)
            return Response(e.toHttp(), e.status)
        except Exception as e:
            traceback.print_exception(e)
            return Response({"error": {"message": str(e)}}, 500)
