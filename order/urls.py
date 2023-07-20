from rest_framework import routers

from order.views import OrderViewSet

router = routers.DefaultRouter()
router.register("order", OrderViewSet)

urlpatterns = [] + router.urls

app_name = "order"
