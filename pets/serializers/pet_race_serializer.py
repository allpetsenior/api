from rest_framework import serializers


class PetRaceSerializer(serializers.Serializer):
    id = serializers.CharField(max_length=100)
    specie = serializers.CharField(max_length=200)
    name = serializers.CharField(max_length=200)
    alias = serializers.CharField(max_length=200)
