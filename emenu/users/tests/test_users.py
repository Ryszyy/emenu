from django.contrib.auth import get_user_model
from django.test import TestCase
from factory import Faker

from emenu.users.tests.factories import UserFactory

User = get_user_model()


class UserModelTest(TestCase):
    def setUp(self):
        self.payload = {
            "email": Faker("email").generate(),
            "password": Faker("password", length=42).generate()
        }

    def test_create_user(self):
        user = User.objects.create(**self.payload)
        self.assertTrue(user.is_active)

    def test_create_superuser(self):
        user = User.objects.create_superuser(**self.payload)
        self.assertTrue(user.is_superuser)

    def test_user_str_repr(self):
        user = UserFactory(email=self.payload["email"])
        self.assertEqual(user.__str__(), self.payload["email"])
        self.assertEqual(user.__repr__(), self.payload["email"])
