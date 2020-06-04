import factory
from emenu.cards.models import Cards, Dishes


class CardFactory(factory.DjangoModelFactory):
    class Meta:
        model = Cards
        django_get_or_create = ('name',)

    name = factory.Sequence(lambda n: f'Card{n}')

    @factory.post_generation
    def dishes(self, create, extracted, **kwargs):
        if not create:
            # Simple build, do nothing.
            return

        if extracted:
            # A list of groups were passed in, use them
            for dish in extracted:
                self.dishes.add(dish)


class DishFactory(factory.DjangoModelFactory):
    class Meta:
        model = Dishes

    name = factory.Sequence(lambda n: "Dish #%s" % n)
    price = factory.Faker("random_int")
    preparation_time = factory.Faker("random_int")