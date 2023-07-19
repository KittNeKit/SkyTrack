from rest_framework import routers

from airport.views import AirportViewSet, RouteViewSet

router = routers.DefaultRouter()
router.register("airport", AirportViewSet)
router.register("route", RouteViewSet)


urlpatterns = [] + router.urls

app_name = "airport"
