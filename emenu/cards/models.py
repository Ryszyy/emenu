from django.db import models
from django.utils.translation import gettext_lazy as _


class Dish(models.Model):
    name = models.CharField(_("name"), max_length=255, blank=False)
    description = models.CharField(_("description"), max_length=255, blank=True)
    price = models.DecimalField(_("price"), decimal_places=2, max_digits=8, default=20.0,
                                help_text=_("Default is 20$"))
    preparation_time = models.PositiveIntegerField(
        _("preparation time"), help_text=_("Counted in minutes, default is 5"), default=5)
    is_vegan = models.BooleanField(_("is vegan"), default=False)
    add_date = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class Card(models.Model):
    name = models.CharField(_('name'), max_length=255, blank=False, unique=True)
    description = models.CharField(_("description"), max_length=255, blank=True)
    dishes = models.ManyToManyField(Dish, related_name="cards")

    add_date = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
