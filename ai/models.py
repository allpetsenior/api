import uuid

from django.db import models
from django.utils.translation import gettext_lazy as _
from core.models import User
from pets.models import Pet


class Recommendation(models.Model):
    pet = models.ForeignKey(Pet, on_delete=models.CASCADE)
    content = models.CharField(max_length=4000)

    class Type(models.TextChoices):
        health = 'HT', _('HEALTH')
        nutrition = 'NT', _('NUTRITION')
        activity = 'AT', _('ACTIVITY')

    type = models.CharField(
        max_length=12,
        choices=Type.choices,
    )

    created_at = models.DateTimeField(auto_now_add=True)
    update_in = models.DateTimeField()


class Feedback(models.Model):
    recommendation = models.OneToOneField(
        Recommendation, on_delete=models.CASCADE)
    is_good = models.BooleanField()


class Chat(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    user = models.ForeignKey(to=User, on_delete=models.CASCADE)
    max_messages = models.IntegerField(default=60)
    remaining_messages = models.IntegerField(default=60)
    reset_in = models.DateTimeField()
