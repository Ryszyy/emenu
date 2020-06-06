import factory

from emenu.cards.models import Card, Dish


class CardFactory(factory.DjangoModelFactory):
    class Meta:
        model = Card
        django_get_or_create = ('name',)

    name = factory.Sequence(lambda n: f'Card{n}')
    description = factory.Sequence(lambda n: "Description #%s" % n)

    @factory.post_generation
    def dishes(self, create, extracted, **kwargs):
        if not create:
            # Simple build, do nothing.
            return

        if extracted:
            # A list of groups were passed in, use them
            for dish in extracted:
                self.dishes.add(dish)


def get_card_payload():
    payload = CardFactory.build().__dict__
    for key in ["id", "add_date", "updated", "_state"]:
        payload.pop(key, None)
    return payload


class DishFactory(factory.DjangoModelFactory):
    class Meta:
        model = Dish

    name = factory.Sequence(lambda n: "Dish #%s" % n)
    description = factory.Sequence(lambda n: "Description #%s" % n)
    price = factory.Faker("random_int")
    preparation_time = factory.Faker("random_int")
