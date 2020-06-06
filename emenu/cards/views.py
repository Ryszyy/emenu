import django_filters
from django.db import models
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import permissions, viewsets
from rest_framework.filters import OrderingFilter

from emenu.cards import serializers
from emenu.cards.models import Card, Dish


class CustomFilterBackend(OrderingFilter):
    def filter_queryset(self, request, queryset, view):
        ordering = self.get_ordering(request, queryset, view)
        if ordering is None:
            return queryset

        new_order = []
        for field in ordering:
            if "dishes" in field:
                queryset = queryset.annotate(num_of_dishes=models.Count("dishes"))
                order = "-num_of_dishes" if field.startswith("-") else "num_of_dishes"
                new_order.append(order)
            if "name" in field:
                new_order.append(field)

        return queryset.order_by(*new_order)


class CustomCardFilter(django_filters.FilterSet):
    class Meta:
        model = Card
        fields = {
            'name': ['exact'],
            'add_date': ['range'],
            'updated': ['range'],
        }

    @classmethod
    def filter_for_lookup(cls, f, lookup_type):
        # override date range lookups
        if isinstance(f, models.DateField) and lookup_type == 'range':
            return django_filters.DateRangeFilter, {}

        # use default behavior otherwise
        return super().filter_for_lookup(f, lookup_type)


class DishViewSet(viewsets.ModelViewSet):
    queryset = Dish.objects.all()
    serializer_class = serializers.DishSerializer
    permission_classes = [permissions.IsAuthenticated]


class CardViewSet(viewsets.ModelViewSet):
    queryset = Card.objects.all()
    serializer_class = serializers.CardSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, ]
    filter_backends = [CustomFilterBackend, DjangoFilterBackend]
    filterset_class = CustomCardFilter
    ordering_fields = ("name", "dishes")
    filterset_fields = ['name', 'add_date', 'updated']
    distinct = True

    def get_queryset(self):
        if not self.request.user.is_authenticated:
            self.queryset = Card.objects.exclude(dishes__exact=None)
        return self.queryset

    def get_serializer_class(self):
        if self.action == "retrieve":
            return serializers.CardDetailSerializer

        return self.serializer_class
