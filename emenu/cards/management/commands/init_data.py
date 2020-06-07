import factory
from django.core.management.base import BaseCommand, CommandError

from emenu.cards.tests.factories import CardFactory, DishFactory
from emenu.users.tests.factories import UserFactory


def create_data():
    for _ in range(50):
        s_dish_factory = factory.Faker("random_int", min=2, max=10).generate() * "DishFactory(), "
        s_dish_factory = s_dish_factory[:-2]
        CardFactory.create(dishes=(eval(s_dish_factory)))
    for _ in range(20):
        UserFactory()
        DishFactory()
        CardFactory()


class Command(BaseCommand):
    help = 'Initializes database with some data'

    def handle(self, *args, **options):
        try:
            create_data()
        except Exception as e:
            raise CommandError(f"Could not initialize data - {e}")
        else:
            self.stdout.write(self.style.SUCCESS("Initialized data"))
