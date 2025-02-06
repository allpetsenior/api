from rest_framework import serializers


class UserSerializer(serializers.Serializer):
    id = serializers.UUIDField()
    name = serializers.CharField(max_length=200)
    last_name = serializers.CharField(max_length=200)
    password = serializers.CharField(max_length=200)
    birth_date = serializers.DateTimeField()

    state = serializers.CharField(
        max_length=5,
    )

    cellphone = serializers.CharField(max_length=200)
    email = serializers.CharField(max_length=200)
