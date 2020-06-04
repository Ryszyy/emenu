# 1. REST API do zarządzania menu
# 2. Możliwość tworzenia wielu wersji kart(menu) o unikalnej nazwie.
# 3. Każda karta może zawierać dowolną liczbę dań.
# 6. API musi być zabezpieczone przed nieautoryzowanym dostępem(po autoryzacji użytkownika)

# 1. Rest API do przeglądania niepustych karta menu.
# 2. Możliwość sortowanie listy po nazwie oraz liczbie dań, za pomocą parametrów GET
# 3. Filtrowanie listy po nazwie oraz okresie dodanie i ostatnie aktualizacji
# 4. Detal karty prezentujący wszystkie dana dotyczące karty oraz dań w karcie.
from django.test import TestCase
from factory import Faker
from emenu.cards.tests.factories import CardFactory


class CardsModelTest(TestCase):
    def test_cards_str(self):
        name = "Vegetarian"
        card = CardFactory(name=name)
        self.assertEqual(str(card), name)
