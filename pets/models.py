import uuid
from django.db import models
from core.models import User


class Pet(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    name = models.CharField(max_length=200)
    specie = models.CharField(max_length=200)
    race = models.CharField(max_length=200)
    sex = models.CharField(max_length=200)
    is_castrated = models.BooleanField()
    color = models.CharField(max_length=200, null=True)
    size = models.CharField(max_length=200)
    activity = models.CharField(max_length=200)
    health_problem = models.CharField(max_length=200)
    medicine = models.CharField(max_length=200, null=True)
    predominant_race = models.CharField(max_length=200, null=True)
    coat = models.CharField(max_length=200, null=True)
    coat_texture = models.CharField(max_length=200, null=True)
    coat_pattern = models.CharField(max_length=200, null=True)
    birth_date = models.DateTimeField()
    weight = models.IntegerField()
    tutor = models.ForeignKey(User, on_delete=models.CASCADE)
