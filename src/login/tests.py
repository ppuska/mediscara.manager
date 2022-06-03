import email
from django.test import TestCase
from django.contrib.auth import authenticate

class AuthTestCase(TestCase):
    def test_login(self):
        user = authenticate(email="manager@medicor.hu", password="manager")

        self.assertIsNotNone(user)
        self.assertTrue(user.is_authenticated)