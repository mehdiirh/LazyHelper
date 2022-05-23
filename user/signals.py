from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User

from . import models


@receiver(post_save, sender=User)
def user_initialization(instance: User, created=False, raw=False, **kwargs):

    if raw:
        return

    # only process creates
    if not created:
        return

    if instance.pk is None:
        return

    models.Profile.objects.get_or_create(user=instance)
