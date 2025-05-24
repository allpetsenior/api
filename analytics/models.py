from uuid import uuid4
from django.db import models

from core.models import User


class Analytic(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4)
    user = models.ForeignKey(to=User, on_delete=models.CASCADE)
    metadata = models.JSONField()
