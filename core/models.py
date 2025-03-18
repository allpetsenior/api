import uuid

from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.translation import gettext_lazy as _
from rest_framework.authtoken.models import Token


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(instance=None, created=False, **kwargs):
  if created:
    Token.objects.create(user=instance)


class User(AbstractUser):
  id = models.UUIDField(primary_key=True, default=uuid.uuid4)
  name = models.CharField(max_length=200)
  last_name = models.CharField(max_length=200)
  password = models.CharField(max_length=200)
  birth_date = models.DateTimeField()

  class Gender(models.TextChoices):
    male = 'MALE', _('MALE')
    female = 'FEMALE', _('FEMALE')
    other = 'OTHER', _('OTHER')

  gender = models.CharField(
      max_length=10,
      choices=Gender.choices,
      default=Gender.male
  )

  class State(models.TextChoices):
    RJ = 'RJ', _('RIO DE JANEIRO')

  state = models.CharField(
      max_length=2,
      choices=State.choices,
      default=State.RJ
  )

  cellphone = models.CharField(max_length=200)
  email = models.EmailField()


class Invite(models.Model):
  class Meta:
    db_table = 'invites'
    verbose_name = 'Convite'
    verbose_name_plural = 'Convites'

  email = models.EmailField(unique=True)
  created_at = models.DateTimeField(auto_created=True)
  user = models.ForeignKey(settings.AUTH_USER_MODEL, models.PROTECT)


class Feedback(models.Model):
  class Meta:
    db_table = 'feedbacks'
    verbose_name = 'Feedback'
    verbose_name_plural = 'Feedbacks'

  class Reaction(models.IntegerChoices):
    SMILE = 5, _('Feliz')
    MEH = 3, _('Normal')
    FROWN = 1, _('Insatisfeito')

  email = models.EmailField(unique=True)
  rating = models.PositiveSmallIntegerField(choices=Reaction.choices)
  text = models.TextField()
  created_at = models.DateTimeField(auto_created=True)
  user = models.ForeignKey(settings.AUTH_USER_MODEL, models.PROTECT)
