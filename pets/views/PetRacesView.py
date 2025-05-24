from django.core.paginator import EmptyPage
from rest_framework.decorators import permission_classes
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
        previous = None
        next_page = None
        try:
            next_page = self.page.next_page_number()
            previous = self.page.previous_page_number()
        except EmptyPage:
            pass

        return Response({
            'next': next_page,
            "previous": previous,
            'count': self.page.paginator.count,
            'results': data
        })


class PetRaces(ListAPIView):
    permission_classes = []
    serializer_class = PetRaceSerializer
    pagination_class = StandardResultsSetPagination

    def get_queryset(self):
        params = self.request.query_params
        obj1 = {}
        obj2 = {}
        specie = params.get("specie")
        name = params.get("name")

        if specie:
            obj1["specie"] = specie
            obj2["specie"] = specie
        if name:
            obj1["name__icontains"] = name
            obj2["alias__icontains"] = name

        return PetRace.objects.filter(**obj1).order_by("name") | PetRace.objects.filter(**obj2).order_by("name")
