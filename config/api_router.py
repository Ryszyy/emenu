from django.conf import settings
from rest_framework.routers import DefaultRouter, SimpleRouter

from emenu.cards.views import DishViewSet

if settings.DEBUG:
    router = DefaultRouter()
else:
    router = SimpleRouter()

router.register("dishes", DishViewSet)


app_name = "api"
urlpatterns = router.urls
