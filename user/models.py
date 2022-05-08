from django.db import models
from django.contrib.auth.models import User

from utils.generators.functions import generate_unique_id


class Profile(models.Model):

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    api_key = models.CharField(max_length=32, null=True, help_text='To change api_key, remove value of'
                                                                   ' this input and save.')

    def save(self, *args, **kwargs):
        if self.api_key is None or len(str(self.api_key)) < 32:
            self.api_key = generate_unique_id(model=Profile, field='api_key')

        super().save(*args, **kwargs)