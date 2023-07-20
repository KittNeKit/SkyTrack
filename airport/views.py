from rest_framework import viewsets
from rest_framework_simplejwt.authentication import JWTAuthentication

from airport.models import Airport, Route
from airport.permissions import IsAdminOrIfUserReadOnly
from airport.serializers import AirportSerializer, RouteSerializer


class AirportViewSet(viewsets.ModelViewSet):
    queryset = Airport.objects.all()
    serializer_class = AirportSerializer
    permission_classes = (IsAdminOrIfUserReadOnly,)
    authentication_classes = (JWTAuthentication,)


class RouteViewSet(viewsets.ModelViewSet):
    queryset = Route.objects.all().select_related("source", "destination")
    serializer_class = RouteSerializer
    permission_classes = (IsAdminOrIfUserReadOnly,)
    authentication_classes = (JWTAuthentication,)

