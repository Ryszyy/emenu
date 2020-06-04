from django.test import TestCase
from factory import Faker
from emenu.cards.tests.factories import DishFactory


class DishesModelTest(TestCase):
    def test_cards_str(self):
        name = "Vegetarian"
        card = DishFactory(name=name)
        self.assertEqual(str(card), name)
