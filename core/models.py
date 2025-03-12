import uuid

from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
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
