from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient, APITestCase

from emenu.cards.models import Dish
from emenu.cards.serializers import DishSerializer
from emenu.cards.tests.factories import DishFactory
from emenu.users.tests.factories import UserFactory


class DishesModelTest(TestCase):
    def test_cards_str(self):
        name = "Special Soup"
        card = DishFactory(name=name)
        self.assertEqual(str(card), name)


class PrivateDishesApi(APITestCase):
    def setUp(self):
        self.url = reverse("api:dish-list")
        self.user = UserFactory()
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

    def test_create_dish(self):
        dish_payload = DishFactory().__dict__
        request = self.client.post(self.url, dish_payload)
        self.assertEqual(request.status_code, status.HTTP_201_CREATED)
        dish = Dish.objects.get(id=request.data["id"])
        serial_dish = DishSerializer(dish)
        self.assertEqual(serial_dish.data, request.data)
