from django.db import models


class Config(models.Model):

    key = models.CharField(max_length=128)
    active = models.BooleanField(default=True)
