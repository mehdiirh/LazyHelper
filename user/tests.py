from django.test import TestCase
from django.contrib.auth.models import User

from .models import Profile


class TestProfile(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_superuser('test_superuser', password='passwd')

    def test_profile_creation(self):
        profile = Profile.objects.filter(user=self.user).first()
        self.assertIsNotNone(profile)
