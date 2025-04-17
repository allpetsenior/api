from rest_framework import serializers


class ChatSerializer(serializers.Serializer):
    id = serializers.CharField()
    max_messages = serializers.IntegerField()
    remaining_messages = serializers.IntegerField()
    reset_in = serializers.DateTimeField()
