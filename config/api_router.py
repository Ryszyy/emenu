from django.conf import settings
from rest_framework.routers import DefaultRouter, SimpleRouter

from emenu.cards import views

if settings.DEBUG:
    router = DefaultRouter()
else:
    router = SimpleRouter()

router.register("dishes", views.DishViewSet)
router.register("cards", views.CardViewSet)


app_name = "api"
urlpatterns = router.urls
