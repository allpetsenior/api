from rest_framework import serializers

from .models import Feedback, Invite, Tip


class TipSerializer(serializers.ModelSerializer):
  class Meta:
    model = Tip
    fields = '__all__'


class UserSerializer(serializers.Serializer):
  id = serializers.UUIDField()
  name = serializers.CharField(max_length=200)
  last_name = serializers.CharField(max_length=200)
  birth_date = serializers.DateTimeField()
  gender = serializers.CharField(max_length=10)
  tip_of_day = TipSerializer()

  state = serializers.CharField(
      max_length=5,
  )

  cellphone = serializers.CharField(max_length=200)
  email = serializers.CharField(max_length=200)


class InviteSerializer(serializers.ModelSerializer):

  class Meta:
    model = Invite
    exclude = ['user']


class FeedbackSerializer(serializers.ModelSerializer):

  class Meta:
    model = Feedback
    exclude = ['user']
