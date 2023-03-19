from unittest import TestCase
from ..models import Profile
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist

username = "test_username"
email = "test@test.com"
password = "test_password"

class TestProfile(TestCase):
    pass