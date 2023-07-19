from rest_framework import routers

from order.views import TicketViewSet, OrderViewSet

router = routers.DefaultRouter()
router.register("order", OrderViewSet)
router.register("ticket", TicketViewSet)


urlpatterns = [] + router.urls

app_name = "order"
