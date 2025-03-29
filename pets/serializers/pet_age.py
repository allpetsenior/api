from rest_framework import serializers


class PetAgeSerializer(serializers.Serializer):
    id = serializers.CharField()
    specie = serializers.CharField()
    size = serializers.CharField()
    age = serializers.IntegerField()
    human_age_in_years = serializers.IntegerField()
