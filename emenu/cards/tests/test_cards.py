import factory
from django.db.models import Count
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient, APITestCase

from emenu.cards.models import Card
from emenu.cards.serializers import CardDetailSerializer, CardSerializer
from emenu.cards.tests.factories import CardFactory, DishFactory, get_card_payload
from emenu.users.tests.factories import UserFactory


def detail_url(recipe_id):
    return reverse('api:card-detail', args=[recipe_id])


def ordering_url(ordering):
    return reverse("api:card-list") + f"?ordering={ordering}"


def create_cards():
    for _ in range(10):
        s_dish_factory = factory.Faker("random_int", min=2, max=10).generate() * "DishFactory(), "
        s_dish_factory = s_dish_factory[:-2]
        CardFactory.create(dishes=(eval(s_dish_factory)))


class CardsModelTest(TestCase):
    def test_cards_str(self):
        name = "Vegetarian"
        card = CardFactory(name=name)
        self.assertEqual(str(card), name)


class PublicCardsApi(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.url = reverse("api:card-list")

    def test_cards_list_not_empty_cards(self):
        empty_card = CardFactory()
        full_card = CardFactory.create(dishes=(DishFactory(),))
        request = self.client.get(self.url)
        self.assertEqual(request.status_code, status.HTTP_200_OK)
        serial_cards = CardSerializer(
            (empty_card, full_card), many=True)
        self.assertNotIn(serial_cards.data[0], request.data)
        self.assertIn(serial_cards.data[1], request.data)

    def test_cards_list_sorting_using_parameters(self):
        create_cards()
        request = self.client.get(ordering_url("dishes,name"))
        self.assertEqual(request.status_code, status.HTTP_200_OK)
        cards = Card.objects.annotate(num_of_dishes=Count('dishes')).order_by("num_of_dishes", "name")

        serial_cards = CardSerializer(cards, many=True)
        self.assertEqual(request.data, serial_cards.data)

        request = self.client.get(ordering_url("name"))
        cards = Card.objects.all().order_by("name")
        serial_cards = CardSerializer(cards, many=True)
        self.assertEqual(request.data, serial_cards.data)

    def test_cards_list_filtering_using_date(self):
        create_cards()
        card_name = "Test Card"
        CardFactory.create(name=card_name, dishes=(DishFactory(),))
        request = self.client.get(self.url, {"name": card_name})
        self.assertEqual(request.status_code, status.HTTP_200_OK)
        card = Card.objects.filter(name=card_name)
        serial_cards = CardSerializer(card, many=True)
        self.assertEqual(request.data, serial_cards.data)

    def test_cards_details_with_dishes(self):
        temp_card = CardFactory.create(dishes=(DishFactory(), DishFactory()))
        url = detail_url(temp_card.id)
        request = self.client.get(url)
        self.assertEqual(request.status_code, status.HTTP_200_OK)

        card = Card.objects.prefetch_related('dishes').get(id=temp_card.id)
        serial_card = CardDetailSerializer(card)
        self.assertEqual(request.data["dishes"], serial_card.data["dishes"])
        self.assertEqual(len(request.data["dishes"]), 2)

    def test_anon_user_cannot_create_cards(self):
        card_payload = get_card_payload()
        request = self.client.post(self.url, card_payload)
        self.assertEqual(request.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateCardsApi(APITestCase):
    def setUp(self):
        self.url = reverse("api:card-list")
        self.user = UserFactory()
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)
        self.card = CardFactory.create()

    def test_retrieve_cards(self):
        CardFactory()
        request = self.client.get(self.url)
        self.assertEqual(request.status_code, status.HTTP_200_OK)
        self.assertEqual(len(request.data), 2)
        request = self.client.get(self.url, id="1")
        self.assertEqual(request.status_code, status.HTTP_200_OK)

    def test_cards_create(self):
        card_payload = get_card_payload()
        request = self.client.post(self.url, card_payload)
        self.assertEqual(request.status_code, status.HTTP_201_CREATED)
        self.assertEqual(card_payload["name"], request.data["name"])

    def test_add_dish_to_card(self):
        dish_payload = [DishFactory().id, DishFactory().id]
        url = detail_url(self.card.id)
        request = self.client.patch(url, {"dishes": dish_payload})
        self.assertEqual(request.status_code, status.HTTP_200_OK)
        self.card.refresh_from_db()
        dishes = self.card.dishes.values_list('id', flat=True)
        for dish in dish_payload:
            self.assertIn(dish, dishes)
