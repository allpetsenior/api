from rest_framework import serializers


class UserSerializer(serializers.Serializer):
    id = serializers.UUIDField()
    name = serializers.CharField(max_length=200)
    last_name = serializers.CharField(max_length=200)
    birth_date = serializers.DateTimeField()
    gender = serializers.CharField(max_length=10)

    state = serializers.CharField(
        max_length=5,
    )

    cellphone = serializers.CharField(max_length=200)
    email = serializers.CharField(max_length=200)
