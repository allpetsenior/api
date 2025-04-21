from rest_framework import serializers as s

from pets.models import *

# class PetRaceSerializer(s.Serializer):
#     id = s.CharField(max_length=200)
#     specie = s.CharField(max_length=200)
#     name = s.CharField(max_length=200)
#     alias = serializers.CharField(max_length=200)


class PetMinMaxWeightSerializer(s.ModelSerializer):

  class Meta:
    model = PetMinMaxWeight
    exclude = ['race']


class PetRaceSerializer(s.ModelSerializer):
    weights = PetMinMaxWeightSerializer(
        many=True, source='petminmaxweight_set')

    class Meta:
        model = PetRace
        fields = '__all__'


class PetSerializer(s.Serializer):
    id = s.CharField(max_length=200)
    name = s.CharField(max_length=200)
    race = PetRaceSerializer()
    color = s.CharField(max_length=200)
    size = s.CharField(max_length=200)
    activity = s.CharField(max_length=200)
    health_problem = s.CharField(max_length=200)
    medicine = s.CharField(max_length=200)
    habitation = s.CharField(max_length=40)
    predominant_race = s.CharField(max_length=200)
    coat = s.CharField(max_length=200)
    coat_texture = s.CharField(max_length=200)
    coat_pattern = s.CharField(max_length=200)
    birth_date = s.DateTimeField()
    weight = s.DecimalField(max_digits=5, decimal_places=2)
    specie = s.CharField(max_length=200)
    sex = s.CharField(max_length=200)
    is_castrated = s.BooleanField()
