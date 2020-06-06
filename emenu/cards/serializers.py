from rest_framework import serializers

from emenu.cards.models import Card, Dish


class DishSerializer(serializers.ModelSerializer):
    class Meta:
        model = Dish
        fields = (
            'id', 'name', 'description', 'price', 'preparation_time',
            'is_vegan', 'add_date', 'updated'
        )
        read_only_fields = ('id', 'add_date', 'updated')


class CardSerializer(serializers.ModelSerializer):
    dishes = serializers.PrimaryKeyRelatedField(
        allow_null=True,
        many=True,
        queryset=Dish.objects.all()
    )

    class Meta:
        model = Card
        fields = (
            'id', 'name', 'description', 'dishes', 'add_date', 'updated'
        )
        read_only_fields = ('id', 'add_date', 'updated')


class CardDetailSerializer(CardSerializer):
    dishes = DishSerializer(many=True, read_only=True)
