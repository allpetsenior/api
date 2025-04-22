from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import ListAPIView
from rest_framework.pagination import PageNumberPagination
from rest_framework.views import Response

from pets.models import PetRace
from pets.serializers.pet_serializer import PetRaceSerializer


class StandardResultsSetPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100

    def get_paginated_response(self, data):
        return Response({
            'next': self.get_next_link(),
            'previous': self.get_previous_link(),
            'count': self.page.paginator.count,
            'results': data
        })


class PetRaces(ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = PetRaceSerializer
    pagination_class = StandardResultsSetPagination

    def get_queryset(self):
        params = self.request.query_params
        data = {}
        specie = params.get("specie")
        name = params.get("name")

        if specie:
            data["specie"] = specie

        if name:
            data["name"] = name

        return PetRace.objects.filter(**data)
