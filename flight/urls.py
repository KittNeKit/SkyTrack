from rest_framework import routers

from flight.views import (
    AirplaneTypeViewSet,
    AirplaneViewSet,
    CrewViewSet,
    FlightViewSet,
)

router = routers.DefaultRouter()
router.register("airplane_type", AirplaneTypeViewSet)
router.register("airplane", AirplaneViewSet)
router.register("crew", CrewViewSet)
router.register("flight", FlightViewSet)


urlpatterns = router.urls

app_name = "departures"
