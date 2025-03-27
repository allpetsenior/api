import traceback

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from v0.errors.app_error import App_Error
from pets.services.get_pet_ages_service import get_pet_ages_service
from pets.serializers.pet_age import PetAgeSerializer


class AgeCalculatorView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            pet_ages = get_pet_ages_service()

            serializer = PetAgeSerializer(pet_ages, many=True)

            return Response({"data": serializer.data})
        except App_Error as e:
            traceback.print_exception(e)
            return Response(e.toHttp(), e.status)
        except Exception as e:
            traceback.print_exception(e)
            return Response({"error": {"message": str(e)}}, 500)
