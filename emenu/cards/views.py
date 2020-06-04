from rest_framework import mixins, permissions, viewsets

from emenu.cards.models import Dish
from emenu.cards.serializers import DishSerializer


class DishViewSet(viewsets.GenericViewSet, mixins.CreateModelMixin):
    queryset = Dish.objects.all()
    serializer_class = DishSerializer
    permission_classes = [permissions.IsAuthenticated]
