from django.db import models
from django.utils.translation import gettext_lazy as _

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
