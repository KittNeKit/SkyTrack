from rest_framework import routers


router = routers.DefaultRouter()
# router.register()


urlpatterns = [] + router.urls
app_name = "user"
