from django.db import models
from django.utils.translation import gettext_lazy as _


class Dishes(models.Model):
    name = models.CharField(_("name"), max_length=255, blank=False)
    description = models.CharField(_("description"), max_length=255,)
    price = models.DecimalField(_("price"), decimal_places=2, max_digits=6, blank=False)
    preparation_time = models.PositiveIntegerField(
        _("preparation time"), help_text=_("Counted in minutes"))
    is_vegan = models.BooleanField(_("is vegan"), default=False)
    add_date = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class Cards(models.Model):
    name = models.CharField(_('name'), max_length=255, blank=True, unique=True)
    description = models.CharField(_("description"), max_length=255)
    dishes = models.ManyToManyField(Dishes, related_name="cards")

    add_date = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
