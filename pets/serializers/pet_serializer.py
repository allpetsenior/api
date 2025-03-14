from rest_framework import serializers


class PetRaceSerializer(serializers.Serializer):
    id = serializers.CharField(max_length=200)
    specie = serializers.CharField(max_length=200)
    name = serializers.CharField(max_length=200)
    alias = serializers.CharField(max_length=200)


class PetSerializer(serializers.Serializer):
    id = serializers.CharField(max_length=200)
    name = serializers.CharField(max_length=200)
    race = PetRaceSerializer()
    color = serializers.CharField(max_length=200)
    size = serializers.CharField(max_length=200)
    activity = serializers.CharField(max_length=200)
    health_problem = serializers.CharField(max_length=200)
    medicine = serializers.CharField(max_length=200)
    predominant_race = serializers.CharField(max_length=200)
    coat = serializers.CharField(max_length=200)
    coat_texture = serializers.CharField(max_length=200)
    coat_pattern = serializers.CharField(max_length=200)
    birth_date = serializers.DateTimeField()
    weight = serializers.DecimalField(max_digits=5, decimal_places=2)
    specie = serializers.CharField(max_length=200)
    sex = serializers.CharField(max_length=200)
    is_castrated = serializers.BooleanField()
